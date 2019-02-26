#! /usr/bin/python3
# -*- coding: utf-8 -*-
# This is the main program
#Ricardos.geral@gmail.com
import os
import datetime
import time
from time import sleep
import threading
import py3nextion_lib  as nxlib    # simple python3 library to use nextion device
import nextionApp as nxApp         # initialization of the components of the Nextion display
import sensor_server as srv        # where data is acquired
import socket                      # to find the IP address
import rw_ini as rw                # read and write in .ini file
import write_csv_data              # write results in csv file (sd card in RPi or in USB drive)
import google_sheets as gsh        # export data to google sheets over internet
import RGBled as LED               # manages the multicolor led
from endbips import test_end       # for Buzzer
import database as db              # for postgresSQL
import camera_timelapse as cm
import movie_timelapse as movie
from find_usb import find_dev

# turn of the led
LED.redOff()    #R
LED.greenOff()  #G
LED.blueOff()   #B

######### make connection to serial UART to read/write NEXTION
ser = nxlib.ser

nxlib.nx_setsys(ser, 'bauds', nxlib.BAUD)  # set default baud (default baud rate of nextion from fabric is 9600)
nxlib.nx_setsys(ser, 'bkcmd',0)            # sets in NEXTION 'no return error/success codes'
nxlib.nx_setcmd_1par(ser,'page',1)         # sets page 1  (page 0 is "not connected")
nxlib.nx_setcmd_2par(ser,'tsw','b0',0)     # disable touch events of b0
nxlib.nx_setcmd_2par(ser,'tsw','txt_status',0)                     # disable touch events of dual button
nxlib.nx_setValue(ser, nxApp.ID_status[0], nxApp.ID_status[1], 0)  # red flag - not ready yet

EndCom = "\xff\xff\xff"             # 3 last bits to end serial communication

####OBTAIN DATA FROM INI FILE WITH DEFAULT INPUTS
ini = rw.read_ini()  # read inputs.ini and parse parameters

#settings page
nxlib.nx_setText(ser, nxApp.ID_filename[0] , nxApp.ID_filename[1] , ini['filename'])
nxlib.nx_setText(ser, nxApp.ID_googlesh[0], nxApp.ID_googlesh[1], ini['googlesh'])
nxlib.nx_setText(ser, nxApp.ID_share_email[0], nxApp.ID_share_email[1], ini['share_email'])
nxlib.nx_setText(ser, nxApp.ID_duration[0] , nxApp.ID_duration[1] , ini['duration'])
nxlib.nx_setText(ser, nxApp.ID_interval[0] , nxApp.ID_interval[1] , ini['interval'])
nxlib.nx_setText(ser, nxApp.ID_no_reads[0] , nxApp.ID_no_reads[1] , ini['no_reads'])

# google_sheets checkbutton
google_sheets = ini['google_sheets']
if google_sheets in ['yes','Yes','YES','y','Y','yep']:
    if gsh.google_creds == True:  # if google credentials are ok
        nxlib.nx_setValue(ser, nxApp.ID_google_sheets[0], nxApp.ID_google_sheets[1], 1)  # value = 1
    else:
        nxlib.nx_setValue(ser, nxApp.ID_google_sheets[0], nxApp.ID_google_sheets[1], 0)  # value = 0

else:  # if it's not indicated or it's 'no'
    nxlib.nx_setValue(ser, nxApp.ID_google_sheets[0], nxApp.ID_google_sheets[1], 0)  # value = 0

# testtype page
test = ini['test_type']
if   test == '1':   #Flow Limiting Erosion Test (FLET)
    nxlib.nx_setValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1], 0)    # r0
elif test == '2':   #Crack Filling Erosion Test (CFET)
    nxlib.nx_setValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1], 1)   # r1
elif test == '3':   #Hole Erosion Test (HET)
    nxlib.nx_setValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1], 2)   # r2
elif test == '4':   #other name
    nxlib.nx_setValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1], 3)   # r3
    nxlib.nx_setText(ser, nxApp.ID_othername[0], nxApp.ID_othername[1],ini['othername'])
else: pass

# send to sensors page the inputs from ini file
nxlib.nx_setText(ser, nxApp.ID_mu[0], nxApp.ID_mu[1],ini['mu'])
nxlib.nx_setText(ser, nxApp.ID_mi[0], nxApp.ID_mi[1],ini['mi'])
nxlib.nx_setText(ser, nxApp.ID_md[0], nxApp.ID_md[1],ini['md'])
nxlib.nx_setText(ser, nxApp.ID_bu[0], nxApp.ID_bu[1],ini['bu'])
nxlib.nx_setText(ser, nxApp.ID_bi[0], nxApp.ID_bi[1],ini['bi'])
nxlib.nx_setText(ser, nxApp.ID_bd[0], nxApp.ID_bd[1],ini['bd'])

# flowtype page
flowmeter = ini['flowmeter_type']
if   flowmeter == '1':   # dual button is selected in eletromagnetic flowmeter
    nxlib.nx_setValue(ser, nxApp.ID_flowmeter[0], nxApp.ID_flowmeter[1], 0) # .val = 0
elif flowmeter == '2':   # turbine flowmeter
    nxlib.nx_setValue(ser, nxApp.ID_flowmeter[0], nxApp.ID_flowmeter[1], 1) # .val = 1
nxlib.nx_setText(ser, nxApp.ID_cf[0], nxApp.ID_cf[1],ini['cf'])

# send to timelapse page the inputs from ini file

if ini['timelapse'] in ['yes','Yes','YES','y','Y','yep', 'true', 'True']:
    nxlib.nx_setValue(ser, nxApp.ID_doTimeLapse[0], nxApp.ID_doTimeLapse[1],1)
else:
    nxlib.nx_setValue(ser, nxApp.ID_doTimeLapse[0], nxApp.ID_doTimeLapse[1], 0)

if ini['video'] in ['yes','Yes','YES','y','Y','yep', 'true', 'True']:
    nxlib.nx_setValue(ser, nxApp.ID_doVideo[0], nxApp.ID_doVideo[1],1)
else:
    nxlib.nx_setValue(ser, nxApp.ID_doVideo[0], nxApp.ID_doVideo[1],0)

if ini['del_images'] in ['yes','Yes','YES','y','Y','yep', 'true', 'True']:
    nxlib.nx_setValue(ser, nxApp.ID_delImages[0], nxApp.ID_delImages[1],1)
else:
    nxlib.nx_setValue(ser, nxApp.ID_delImages[0], nxApp.ID_delImages[1],0)

if ini['control_video'] == 0 or ini['control_video'] in ['freq', 'Freq', 'frequency', 'Frequency','fps', 'FPS']:
    nxlib.nx_setValue(ser, nxApp.ID_choiceVideoDur[0], nxApp.ID_choiceVideoDur[1], 0)
else:
    nxlib.nx_setValue(ser, nxApp.ID_choiceVideoDur[0], nxApp.ID_choiceVideoDur[1], 1)

nxlib.nx_setText(ser, nxApp.ID_freqPics[0], nxApp.ID_freqPics[1],ini['freq'])
nxlib.nx_setText(ser, nxApp.ID_maxVideoDur[0], nxApp.ID_maxVideoDur[1],ini['max_videoDur'])

ratioVideoTest=int(ini['interval'])*int(ini['freq'])
nxlib.nx_setText(ser, nxApp.ID_ratioVideoTest[0], nxApp.ID_ratioVideoTest[1],str(ratioVideoTest))


videoDur=round(int(ini['duration'])/ratioVideoTest,1)
nxlib.nx_setText(ser, nxApp.ID_videoDur[0], nxApp.ID_videoDur[1], str(videoDur))

nxlib.nx_setText(ser, nxApp.ID_testDur[0], nxApp.ID_testDur[1],ini['duration'])



##########
## display Ip in page 1 of NEXTION
def get_ip_address():  # get the (local) ip_address of the raspberry pi
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip_address = s.getsockname()[0]
        s.close()
    except:
        ip_address ='No internet connection'
    return ip_address

ip = get_ip_address()
nxlib.nx_setText(ser, nxApp.ID_ip[0], nxApp.ID_ip[1], ip)
print('Current IP: {}'.format(ip))

##########

def input_settings(): # inputs from 'settings' and 'testType' pages
    filename  = nxlib.nx_getText(ser, nxApp.ID_filename[0], nxApp.ID_filename[1])
    googlesh = nxlib.nx_getText(ser, nxApp.ID_googlesh[0], nxApp.ID_googlesh[1])
    share_email = nxlib.nx_getText(ser, nxApp.ID_share_email[0], nxApp.ID_share_email[1])
    if gsh.google_creds == True:  # if credentials are ok
        chk_google = nxlib.nx_getValue(ser, nxApp.ID_google_sheets[0], nxApp.ID_google_sheets[1])
        duration = nxlib.nx_getText(ser, nxApp.ID_duration[0], nxApp.ID_duration[1])
    else:  # if credentials are not working the check box is not selected
        chk_google = 0
        duration = '0'

    interval  = nxlib.nx_getText(ser, nxApp.ID_interval[0], nxApp.ID_interval[1])
    no_reads  = nxlib.nx_getText(ser, nxApp.ID_no_reads[0], nxApp.ID_no_reads[1])
    if chk_google == 1:
        google_sheets = "yes"  # value = 1
    else:  # if it's not indicated or if no is indicated
        google_sheets = "no"  # value = 0
    #test type
    rg  =  nxlib.nx_getValue(ser, nxApp.ID_rg[0],nxApp.ID_rg[1])
    if   rg  == 0: testtype = '1'; othername = ''  #r0
    elif rg  == 1: testtype = '2'; othername = ''  #r1
    elif rg  == 2: testtype = '3'; othername = ''  #r2
    elif rg  == 3: testtype = '4'; othername = nxlib.nx_getText(ser, nxApp.ID_othername[0], nxApp.ID_othername[1])# r3
    else:
        print('unable to determine test type!')
        testtype = '4'; othername = 'something is wrong!'
    lastip  = nxlib.nx_getText(ser, nxApp.ID_ip[0], nxApp.ID_ip[1])

    return{
        'filename'      : filename,
        'googlesh'      : googlesh,
        'share_email'   : share_email,
        'google_sheets' : google_sheets,
        'duration'      : duration,
        'interval'      : interval,
        'no_reads'      : no_reads,
        'test_type'     : testtype,
        'othername'     : othername,
        'lastip'        : lastip
        }

def input_analog():   #inputs from page "sensors", page "flowmeter" and page timelapse
    mu     =   nxlib.nx_getText(ser, nxApp.ID_mu[0], nxApp.ID_mu[1])
    mi     =   nxlib.nx_getText(ser, nxApp.ID_mi[0], nxApp.ID_mi[1])
    md     =   nxlib.nx_getText(ser, nxApp.ID_md[0], nxApp.ID_md[1])
    bu     =   nxlib.nx_getText(ser, nxApp.ID_bu[0], nxApp.ID_bu[1])
    bi     =   nxlib.nx_getText(ser, nxApp.ID_bi[0], nxApp.ID_bi[1])
    bd     =   nxlib.nx_getText(ser, nxApp.ID_bd[0], nxApp.ID_bd[1])

    flowmeter = nxlib.nx_getValue(ser, nxApp.ID_flowmeter[0], nxApp.ID_flowmeter[1])

    if flowmeter == 0: # eletromagnetic flowmeter
        flowmeter_type = '1'
    elif flowmeter == 1:
        flowmeter_type = '2'
    else:
        flowmeter_type ='2'

    cf  =   nxlib.nx_getText(ser, nxApp.ID_cf[0], nxApp.ID_cf[1])

    timelapse     = nxlib.nx_getValue(ser, nxApp.ID_doTimeLapse[0], nxApp.ID_doTimeLapse[1])
    video         = nxlib.nx_getValue(ser, nxApp.ID_doVideo[0], nxApp.ID_doVideo[1])
    del_images    = nxlib.nx_getValue(ser, nxApp.ID_delImages[0], nxApp.ID_delImages[1])
    control_video = nxlib.nx_getValue(ser, nxApp.ID_choiceVideoDur[0], nxApp.ID_choiceVideoDur[1])
    freq          = nxlib.nx_getText(ser, nxApp.ID_freqPics[0], nxApp.ID_freqPics[1])
    max_videoDur  = nxlib.nx_getText(ser, nxApp.ID_maxVideoDur[0], nxApp.ID_maxVideoDur[1])

    return  {
        'mu'   : mu,
        'mi'   : mi,
        'md'   : md,
        'bu'   : bu,
        'bi'   : bi,
        'bd'   : bd,
        'flowmeter_type': flowmeter_type,
        'cf': cf,
        'timelapse':timelapse,
        'video':video,
        'del_images':del_images,
        'control_video':control_video,
        'freq':freq,
        'max_videoDur':max_videoDur,

    }

def display_analog(data):  #outputs
    #inputs from page "sensors"
    nxlib.nx_setText(ser, nxApp.ID_vu[0],   nxApp.ID_vu[1],str(round(data['v_up']*1000)))
    nxlib.nx_setText(ser, nxApp.ID_vi[0],   nxApp.ID_vi[1],str(round(data['v_int']*1000)))
    nxlib.nx_setText(ser, nxApp.ID_vd[0],   nxApp.ID_vd[1],str(round(data['v_down']*1000)))
    nxlib.nx_setText(ser, nxApp.ID_vturb[0],nxApp.ID_vturb[1],str(data['ana_turb']))
    nxlib.nx_setText(ser, nxApp.ID_baru[0], nxApp.ID_baru[1],str(data['bar_up']*1000))
    nxlib.nx_setText(ser, nxApp.ID_bari[0], nxApp.ID_bari[1],str(data['bar_int']*1000))
    nxlib.nx_setText(ser, nxApp.ID_bard[0], nxApp.ID_bard[1],str(data['bar_down']*1000))
    nxlib.nx_setText(ser, nxApp.ID_ntu[0],  nxApp.ID_ntu[1],str(data['turb']))
    nxlib.nx_setText(ser, nxApp.ID_flowrate[0],  nxApp.ID_flowrate[1],str(data['flow']))


def display_sensors(data):   #outputs of "record" page
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d, %H:%M")

    nxlib.nx_setText(ser, nxApp.ID_datetime[0], nxApp.ID_datetime[1],date_time)
    nxlib.nx_setText(ser, nxApp.ID_pu[0], nxApp.ID_pu[1],str(data['mmH2O_up']))
    nxlib.nx_setText(ser, nxApp.ID_pi[0], nxApp.ID_pi[1],str(data['mmH2O_int']))
    nxlib.nx_setText(ser, nxApp.ID_pd[0], nxApp.ID_pd[1],str(data['mmH2O_down']))
    nxlib.nx_setText(ser, nxApp.ID_turb[0], nxApp.ID_turb[1],str(data['turb']))
    nxlib.nx_setText(ser, nxApp.ID_liters[0], nxApp.ID_liters[1],str(round(data['liters'],1)))
    nxlib.nx_setText(ser, nxApp.ID_flow[0], nxApp.ID_flow[1],str(data['flow']))
    nxlib.nx_setText(ser, nxApp.ID_tw[0], nxApp.ID_tw[1],str(data['water_temp']))
    nxlib.nx_setText(ser, nxApp.ID_ta[0], nxApp.ID_ta[1],str(data['air_temp']))
    nxlib.nx_setText(ser, nxApp.ID_hd[0], nxApp.ID_hd[1],str(data['air_hum']))
    nxlib.nx_setText(ser, nxApp.ID_pa[0], nxApp.ID_pa[1],str(data['air_pres']))


#DEFAULT INPUTS #####################
#ser.reset_output_buffer()
inp = input_settings()
inp.update(input_analog())  #all inputs (adds elements to previous dictionary)

#####################
zerou, zeroi, zerod = 0, 0, 0  # always start with zero pressure equal to zero (no shift of the calibration line)
#####################

nxlib.nx_setcmd_2par(ser,'tsw','b0',1)    # re(enable) touch events of page 1
nxlib.nx_setValue(ser, nxApp.ID_status[0], nxApp.ID_status[1], 1)  # green flag - ok to continue

####

def read_display(e_rd): #read and display data in page "sensors"
    if inp['test_type'] == "3":  # if HET test is the selection
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_vi', 0)
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_bari', 0)
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_mi', 0)
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_bi', 0)

    else:
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_vi', 1)
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_bari', 1)
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_mi', 1)
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_bi', 1)

    while end_rd.is_set() == False:
        e_rd.wait()         # restart thread t_rd
        print('read running')
        data=srv.get_data(1,                    #int(inp['interval'])
                          float(inp['mu']), float(inp['mi']), float(inp['md']),
                          float(inp['bu']), float(inp['bi']), float(inp['bd']),
                          zerou, zeroi, zerod, inp['test_type'],
                          inp['flowmeter_type'], inp['cf'])
        display_analog(data)
        #sleep(int(inp['interval']))
        sleep(1)  # in read_display
##################

def read_display_write(e_rdw): # read and display data in page "record" and write to file
    global stop, con, cur
    global takephoto_flag

    #first, check if HET test is selected
    if inp['test_type'] == '3':  # if HET test is the selection
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_pi', 0)
    else:
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_pi', 1)

    # first write in the inputs.ini file the inputs (that will be the default values next time)
    rw.write_ini(inp['filename'],inp['googlesh'], inp['share_email'], inp['google_sheets'],
                 inp['duration'],inp['interval'], inp['no_reads'],
                 inp['test_type'], inp['othername'],
                 inp['mu'],inp['bu'],inp['mi'],inp['bi'],inp['md'],inp['bd'],
                 inp['flowmeter_type'], inp['cf'],
                 inp['timelapse'],inp['video'],inp['del_images'],inp['control_video'],inp['freq'],inp['max_videoDur'],
                 inp['lastip'])

    # obtain the selected worksheet in the google spreadsheet and share it
    export_google = inp['google_sheets']
    if export_google in ('yes', 'Yes', 'YES', 'y', 'Y', 'yep') and gsh.google_creds == True:
        wks = gsh.spreadsheet_worksheet(ssheet_title=inp['googlesh'],
                                        wsheet_title=inp['filename'],
                                        share_email=inp['share_email'])

    e_rdw.wait()
    row = 1
    zero_vol = 0

    #### required to capture the photos
    testname = inp['filename']

    if testname[-4:] != '.csv':
        testname= testname + '.csv'

    checkpath = find_dev('/media/pi/', testname)  # see if usb flash drive is connected
    if checkpath =="":         # If there is no storage device, write on disk (RPi sd card) in /srv/EROSTESTS/<testname>
        path = os.path.join('/srv/EROSTESTS', testname[:-4])
    else:
        path = os.path.join(checkpath, testname[:-4])
    picsLocation = path + '_timelapse_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M"))

    # determine test type
    rg = nxlib.nx_getValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1])
    if rg == 0:
        testtype = 'HET'
    elif rg == 1:
        testtype = 'FLET'
    elif rg == 2:
        testtype = 'CFET'
    elif rg == 3:
        testtype =  nxlib.nx_getText(ser, nxApp.ID_othername[0], nxApp.ID_othername[1])  # r3
    else:
        testtype = 'undetermined'
    #####

    # check if timelapse, movie and delete photos are selected
    doTimelapse = nxlib.nx_getValue(ser, nxApp.ID_doTimeLapse[0], nxApp.ID_doTimeLapse[1])   # 1 = yes
    doMovie     = nxlib.nx_getValue(ser, nxApp.ID_doVideo[0], nxApp.ID_doVideo[1])
    delImages   = nxlib.nx_getValue(ser, nxApp.ID_delImages[0], nxApp.ID_delImages[1])
    # parameters required for the video
    control = nxlib.nx_getValue(ser, nxApp.ID_choiceVideoDur[0], nxApp.ID_choiceVideoDur[1])
    freq = nxlib.nx_getText(ser, nxApp.ID_freqPics[0], nxApp.ID_freqPics[1])
    max_vid_dur = nxlib.nx_getText(ser, nxApp.ID_maxVideoDur[0], nxApp.ID_maxVideoDur[1])
    interval = nxlib.nx_getText(ser, nxApp.ID_interval[0], nxApp.ID_interval[1])


    while end_rdw.is_set() == False and time.time() < stop+int(inp['interval']):
        if time.time() < stop+int(inp['interval']):
            LED.greenOn()
            e_rdw.wait()
            current = time.time()
            elapsed = current - start   # restart thread t_rdw
            elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            autostop =  time.strftime("%H:%M:%S", time.localtime(stop))
            print("write running")
            data=srv.get_data(int(inp['interval']),
                              float(inp['mu']), float(inp['mi']), float(inp['md']),
                              float(inp['bu']), float(inp['bi']), float(inp['bd']),
                              zerou, zeroi, zerod, inp['test_type'], inp['flowmeter_type'], inp['cf'])

            if inp['flowmeter_type'] != "1":  # only if the turbine flowmeter is selected
                if current < start+2:   # zero flowrate at start.
                  zero_vol= data['liters']
                  data['flow'] = 0
                data['liters'] = data['liters']-zero_vol

            write_csv_data.write_data(data = data, data_file = inp['filename'])
            ip = get_ip_address()
            if ip != 'No internet connection':
                #insert a new row in the database in Heroku (only when there is internet)
                    cur.execute("INSERT INTO testdata(date_time, duration, mmH2O_up, mmH2O_int, mmH2O_down, turb, flow, volume) "
                           "VALUES(to_timestamp('{} {}', 'YYYY-MM-DD HH24:MI:SS') ,%s,{},{},{},{},{},{});".format(
                                data['date'], data['time'],
                                data['mmH2O_up'],data['mmH2O_int'],data['mmH2O_down'],data['turb'],data['flow'],
                                data['liters'],inp['interval']),
                                [elapsed,]
                          )

            display_sensors(data)  # display in NEXTION monitor


            ID_elapsed = nxApp.get_Ids('record', 'txt_duration')
            nxlib.nx_setText(ser, ID_elapsed[0], ID_elapsed[1], elapsed)
            ID_autostop = nxApp.get_Ids('record', 'txt_autostop')
            if int(inp['duration']) == 0:
                nxlib.nx_setText(ser, ID_autostop[0], ID_autostop[1], '--:--:--')
            else:
                nxlib.nx_setText(ser, ID_autostop[0], ID_autostop[1], autostop)
            if export_google in ['yes', 'Yes', 'YES', 'y', 'Y', 'yep'] and gsh.google_creds == True:
                gsh.write_gsh(data, row, wks)
                row += 1
            LED.greenOff()

            if ip != 'No internet connection':
                delay = 0.16 # interval to write down  the readings--  NOTE: -0.16 s because of the time to write values in the database
            else:
                delay=0

            # time to timelapse :)

            if doTimelapse == 1:
                # take picture in a different threat
                t_pics = cm.capture(picsLocation, testname[:-4], testtype, elapsed, data['flow'])
                t_pics.start()
                #t_pics.join()  # takes too long. don't use

            sleep(float(inp['interval'])-delay)  # Interval between records


    ### time to make video
    if doMovie == 1:
        # make video in a separate thread
        t_movie = movie.makemovie(picsLocation, testname[:-4], control, freq, max_vid_dur, elapsed, interval)
        t_movie.start()

        if delImages == 1:
            # delete images
            #todo
            pass

    # disconnect from database
    test_end() # morse code sounds to alert for final test

    cur.close()
    con.close()

    end_rdw.set()
    e_rdw.clear()

    nxlib.nx_setcmd_1par(ser, 'page', 'credits')
    ip = get_ip_address()
    nxlib.nx_setValue(ser, nxApp.ID_status[0], nxApp.ID_status[1], 1)  # green flag
    nxlib.nx_setText(ser, nxApp.ID_ip[0], nxApp.ID_ip[1], ip)

##################
# update all inputs previous 'analog' and 'sensors' page
def input_update():
    # update the inputs in settings page
    inp['filename'] = nxlib.nx_getText(ser, nxApp.ID_filename[0], nxApp.ID_filename[1])
    inp['googlesh'] = nxlib.nx_getText(ser, nxApp.ID_googlesh[0], nxApp.ID_googlesh[1])
    inp['share_email'] = nxlib.nx_getText(ser, nxApp.ID_share_email[0], nxApp.ID_share_email[1])
    if nxlib.nx_getValue(ser, nxApp.ID_google_sheets[0], nxApp.ID_google_sheets[1]) == 1:
        inp['google_sheets'] = "yes"  # value = 1
    else:  # if it's not indicated or if no is indicated
        inp['google_sheets'] = "no"  # value = 0
    inp['duration'] = nxlib.nx_getText(ser, nxApp.ID_duration[0], nxApp.ID_duration[1])
    inp['interval'] = nxlib.nx_getText(ser, nxApp.ID_interval[0], nxApp.ID_interval[1])
    inp['no_reads'] = nxlib.nx_getText(ser, nxApp.ID_no_reads[0], nxApp.ID_no_reads[1])

    ######################
    # test type
    rg = nxlib.nx_getValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1])
    if rg == 0:  # r0
        inp['test_type'] = '1'
    elif rg == 1:# r1
        inp['test_type'] = '2'
    elif rg == 2:# r2
        inp['test_type'] = '3'
    elif rg == 3:# r3
        inp['test_type'] = '4'
        inp['othername'] = nxlib.nx_getText(ser, nxApp.ID_othername[0], nxApp.ID_othername[1])
    else:
        print('unable to determine test type!')

    # flowmeter type
    flowmeter = nxlib.nx_getValue(ser, nxApp.ID_flowmeter[0], nxApp.ID_flowmeter[1])
    if flowmeter == 0:
        inp['flowmeter_type'] = '1'
    else:
        inp['flowmeter_type'] = '2'
    inp['cf'] = nxlib.nx_getText(ser, nxApp.ID_cf[0], nxApp.ID_cf[1])

    # timelapse
    doTimeLapse = nxlib.nx_getValue(ser, nxApp.ID_doTimeLapse[0], nxApp.ID_doTimeLapse[1])
    if doTimeLapse == 1: #checkbox selected
        inp['timelapse'] = 'yes'
    else:
        inp['timelapse'] = 'no'

    doVideo = nxlib.nx_getValue(ser, nxApp.ID_doVideo[0], nxApp.ID_doVideo[1])
    if doVideo == 1: #checkbox selected
        inp['video'] = 'yes'
    else:
        inp['video'] = 'no'

    delImages = nxlib.nx_getValue(ser, nxApp.ID_delImages[0], nxApp.ID_delImages[1])
    if delImages == 1: #checkbox selected
        inp['del_images'] = 'yes'
    else:
        inp['del_images'] = 'no'

    choiceVideoDur = nxlib.nx_getValue(ser, nxApp.ID_choiceVideoDur[0], nxApp.ID_choiceVideoDur[1])
    if choiceVideoDur == 0: #checkbox selected
        inp['control_video'] = 'Frequency'
    else:
        inp['control_video'] = 'Max_Duration'

    inp['freq'] = nxlib.nx_getText(ser, nxApp.ID_freqPics[0], nxApp.ID_freqPics[1])
    inp['max_videoDur'] = nxlib.nx_getText(ser, nxApp.ID_maxVideoDur[0], nxApp.ID_maxVideoDur[1])

def detect_touch(e_rd, e_rdw):

    look_touch = 1  # in seconds
    print("detecting serial every {} second(s) ...".format(look_touch))
    global t_rdw, p
    while True:
        try:
            touch=ser.read_until(EndCom)
            if  hex(touch[0]) == '0x65':  #  touch event. If it's empty, do nothing
                pageID_touch = touch[1]
                compID_touch = touch[2]
                event_touch = touch[3]
                print("page= {}, component= {}, event= {}".format(pageID_touch,compID_touch,event_touch))

                if (pageID_touch, compID_touch) == (1, 2):  # ip refresh (comp2) in page 1 is pressed
                    ip=get_ip_address()
                    nxlib.nx_setText(ser, nxApp.ID_ip[0], nxApp.ID_ip[1], ip)

                elif (pageID_touch, compID_touch) == (2, 2):  # button set sensors (comp2) in page 2 is pressed

                    nxlib.nx_setcmd_2par(ser, 'tsw', 'bt_timelapse', 0)  # lock touch for page 5 (sensors) to give time to first

                    end_rd.clear()
                    input_update()
                    srv.init(int(inp['no_reads']),int(inp['no_reads']), inp['flowmeter_type'])  # the interval between displays in monitor should be 1 second, but no_reads does not change
                    t_rd = threading.Thread(target=read_display, name='Read/Display', args=(e_rd,))
                    t_rd.start()

                    sleep(1)  # necessary to allow enough time to start the 1º read of the ads1115 and sensor temp
                    e_rd.set()  # start read_display()
                    nxlib.nx_setcmd_2par(ser, 'tsw', 'bt_timelapse', 1)  # re(enable) touch events of page 5

                elif (pageID_touch,compID_touch) == (2,3):  # button start record (comp3) in page 2 is pressed
                    end_rdw.clear()
                    global start, stop, con, cur
                    input_update()
                    srv.init(int(inp['interval']),
                             int(inp['no_reads']),
                             inp['flowmeter_type'])
                    t_rdw = threading.Thread(target=read_display_write, name='Read/Write/Display', args=(e_rdw,))
                    t_rdw.start()
                    sleep(1)  # necessary to allow enough time to start the 1º read of the ads1115 and sensor temp

                    # connect to databases and clean data from tables
                    # deletes all data from the tables in the database
                    try:
                        con, cur = db.connect_db()

                        cur.execute("DELETE FROM testdata;")
                        cur.execute("DELETE FROM testinputs;")

                        # insert a new row in the database in Heroku
                        cur.execute(
                            "INSERT INTO testinputs (start, test_name, rec_interval, test_type, mu, bu, mi, bi, md, bd) "
                            "VALUES (to_timestamp('{}', 'YYYY-MM-DD HH24:MI') , %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(datetime.datetime.now()),
                            [inp['filename'], inp['interval'], inp['test_type'],
                             inp['mu'], inp['bu'], inp['mi'], inp['bi'], inp['md'], inp['bd'],
                             ])

                        con.commit()
                        cur.execute('rollback;')
                    except:
                        pass

                    e_rdw.set()        #start read_write_display()
                    start = time.time()
                    if int(inp['duration']) == 0:
                        stop = start + 86400 # 'forever', 2 months = 86400 min
                    else:
                        stop = start + int(inp['duration']) * 60  # seconds

                elif (pageID_touch,compID_touch) == (5,3):  # button set zero pressures (comp2) in page 5 is pressed
                    # shown up a text component saying: wait ...

                    global zerou, zeroi, zerod
                    e_rd.clear()
                    sleep(1.5)
                    inp['mu'] = nxlib.nx_getText(ser, nxApp.ID_mu[0], nxApp.ID_mu[1])
                    inp['bu'] = nxlib.nx_getText(ser, nxApp.ID_bu[0], nxApp.ID_bu[1])
                    if inp['test_type'] != '3':
                        inp['mi'] = nxlib.nx_getText(ser, nxApp.ID_mi[0], nxApp.ID_mi[1])
                        inp['bi'] = nxlib.nx_getText(ser, nxApp.ID_bi[0], nxApp.ID_bi[1])

                    inp['bd'] = nxlib.nx_getText(ser, nxApp.ID_bd[0], nxApp.ID_bd[1])
                    inp['md'] = nxlib.nx_getText(ser, nxApp.ID_md[0], nxApp.ID_md[1])

                    zero = srv.zero_press(float(inp['mu']), float(inp['mi']), float(inp['md']),
                                          float(inp['bu']), float(inp['bi']), float(inp['bd']), inp['test_type'])

                    zerou = zero[0]
                    zeroi = zero[1]
                    zerod = zero[2]

                    if inp['test_type'] == "3":  # if HET test is the selection
                        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_vi', 0)
                        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_bari', 0)
                        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_mi', 0)
                        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_bi', 0)

                    else:
                        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_vi', 1)
                        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_bari', 1)
                        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_mi', 1)
                        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_bi', 1)

                    e_rd.set()

                elif (pageID_touch, compID_touch) == (5, 4):  # button refresh calibration. (comp4) in page 5 is pressed
                    e_rd.clear()
                    sleep(1) # give time to pause read
                    inp['mu']    = nxlib.nx_getText(ser, nxApp.ID_mu[0],    nxApp.ID_mu[1])
                    inp['bu']    = nxlib.nx_getText(ser, nxApp.ID_bu[0],    nxApp.ID_bu[1])
                    if inp['test_type'] != '3':
                        inp['mi'] = nxlib.nx_getText(ser, nxApp.ID_mi[0],    nxApp.ID_mi[1])
                        inp['bi'] = nxlib.nx_getText(ser, nxApp.ID_bi[0], nxApp.ID_bi[1])
                    inp['md']    = nxlib.nx_getText(ser, nxApp.ID_md[0],    nxApp.ID_md[1])
                    inp['bd']    = nxlib.nx_getText(ser, nxApp.ID_bd[0],    nxApp.ID_bd[1])
                    e_rd.set()


                elif (pageID_touch, compID_touch) == (5, 21):  # button timelapse is selected (comp21) in page 5 is pressed

                    while True: # this loop is to estimate the duration of the video
                        ratioVideoTest = float(nxlib.nx_getText(ser, nxApp.ID_ratioVideoTest[0], nxApp.ID_ratioVideoTest[1]))
                        testDur = float(nxlib.nx_getText(ser, nxApp.ID_testDur[0], nxApp.ID_testDur[1]))
                        duration_min= testDur/ratioVideoTest  # in minutes
                        # convert to string in form hh:mm:s
                        seconds = duration_min * 60
                        minutes, seconds = divmod(seconds, 60)
                        hours, minutes = divmod(minutes, 60)
                        duration_srt = "%02d:%02d:%02d" % (hours, minutes, seconds)
                        nxlib.nx_setText(ser, nxApp.ID_videoDur[0], nxApp.ID_videoDur[1], duration_srt)
                        try:
                            touch = ser.read_until(EndCom)
                            if hex(touch[0]) == '0x65':  # touch event. If it's empty, do nothing
                                pageID_touch = touch[1]
                                compID_touch = touch[2]
                                event_touch = touch[3]
                                print("page= {}, component= {}, event= {}".format(pageID_touch, compID_touch, event_touch))

                                if (pageID_touch, compID_touch) == (7, 6):
                                    break
                        except:
                            pass


                elif (pageID_touch, compID_touch) == (6, 1):  # back button in flowmeter type selection (comp1) in page 5 is pressed
                # the idea is to stop and restart the threads so that the eventual new flowmeter type can be active
                    end_rd.set()
                    t_rd.join()
                    e_rd.clear()

                    end_rd.clear()
                    input_update()
                    srv.init(int(inp['interval']), int(inp['no_reads']), inp['flowmeter_type'])
                    t_rd = threading.Thread(target=read_display, name='Read/Display', args=(e_rd,))
                    t_rd.start()

                    sleep(1)  # necessary to allow enough time to start the 1º read of the ads1115 and sensor temp
                    e_rd.set()  # start read_display()

                elif (pageID_touch,compID_touch) == (5,1):  # back button leave analog sensors page (comp 1) in page 5 is pressed

                    # write in the inputs.ini file the inputs (that will be the default values next time)
                    rw.write_ini(inp['filename'], inp['googlesh'], inp['share_email'], inp['google_sheets'],
                                 inp['duration'], inp['interval'], inp['no_reads'],
                                 inp['test_type'], inp['othername'],
                                 inp['mu'], inp['bu'], inp['mi'], inp['bi'], inp['md'], inp['bd'],
                                 inp['flowmeter_type'], inp['cf'],
                                 inp['timelapse'], inp['video'], inp['del_images'], inp['control_video'], inp['freq'], inp['max_videoDur'],
                                 inp['lastip'])

                    end_rd.set()
                    t_rd.join()
                    e_rd.clear()

                elif (pageID_touch,compID_touch) == (5,2):  # Home button leave analog sensors page (comp 2) in page 5 is pressed
                    end_rd.set()
                    t_rd.join()
                    e_rd.clear()
                    ip = get_ip_address()
                    nxlib.nx_setValue(ser, nxApp.ID_status[0], nxApp.ID_status[1], 1)  # green flag
                    nxlib.nx_setText(ser, nxApp.ID_ip[0], nxApp.ID_ip[1], ip)

                elif (pageID_touch,compID_touch) == (9,1):  # button confirm exit (comp 1) in page 8 is pressed
                    end_rdw.set()
                    t_rdw.join()
                    e_rdw.clear()

                    LED.magentaOn()
                    sleep(1)
                    LED.magentaOff()

                    ip = get_ip_address()
                    nxlib.nx_setValue(ser, nxApp.ID_status[0], nxApp.ID_status[1], 1)  # green flag
                    nxlib.nx_setText(ser, nxApp.ID_ip[0], nxApp.ID_ip[1], ip)

                    # disconnect from database
                    cur.close()
                    con.close()

            sleep(look_touch)  ### timeout the bigger the larger the chance of missing a push
        except:
            pass

######################
################EVENTS
e_rd = threading.Event()
e_rdw = threading.Event()

end_rd = threading.Event()
end_rdw = threading.Event()

# THREAD - DETECT push buttons
t_serialread = threading.Thread(target=detect_touch, name='read serial',args=(e_rd,e_rdw,))
t_serialread.start()