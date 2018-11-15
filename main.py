#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import datetime
import numpy as np
import time
from time import sleep
import threading
import py3nextion_lib  as nxlib    # simple python3 library to use nextion device
import nextionApp as nxApp # initialization of the components
import sensor_server as srv # where data is acquired
import socket
import rw_ini as rw
import write_csv_data
import google_sheets as gsh
import RGBled as LED
from endbips import test_end # for Buzzer
import database as db

######### make connection to serial UART to read/write NEXTION
ser = nxlib.ser
# ser = serial.Serial(port='/dev/ttyAMA0', baudrate = nxlib.BAUD,
#                     parity=serial.PARITY_NONE,
#                     stopbits=serial.STOPBITS_ONE,
#                     bytesize=serial.EIGHTBITS,
#                     timeout=0.15)

nxlib.nx_setsys(ser, 'bauds', nxlib.BAUD)  # set default baud (default baud rate of nextion from fabric is 9600)
nxlib.nx_setsys(ser, 'bkcmd',0)     # sets in NEXTION 'no return error/success codes'
nxlib.nx_setcmd_1par(ser,'page',1)  # sets page 1  (page 0 is "not connected")
nxlib.nx_setcmd_2par(ser,'tsw','b0',0)    # disable touch events of b0
nxlib.nx_setcmd_2par(ser,'tsw','txt_status',0)    # disable touch events of dual button
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
test = ini['testtype']
if   test == '1':   #Flow Limiting Erosion Test (FLET)
    nxlib.nx_setValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1], 0)    # r0
elif test == '2':   #Crack Filling Erosion Test (CFET)
    nxlib.nx_setValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1], 1)   # r1
elif test == '3':   #Hole Erosion Test (HET)
    nxlib.nx_setValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1], 2)   # r2
elif test == '4':   #other name
    nxlib.nx_setValue(ser, nxApp.ID_rg[0], nxApp.ID_rg[1], 3)   # r3
    nxlib.nx_setText(ser, nxApp.ID_othername[0], nxApp.ID_othername[1],ini['othername'])
else:
    pass

# analog page

nxlib.nx_setText(ser, nxApp.ID_mu[0], nxApp.ID_mu[1],ini['mu'])
nxlib.nx_setText(ser, nxApp.ID_mi[0], nxApp.ID_mi[1],ini['mi'])
nxlib.nx_setText(ser, nxApp.ID_md[0], nxApp.ID_md[1],ini['md'])
nxlib.nx_setText(ser, nxApp.ID_bu[0], nxApp.ID_bu[1],ini['bu'])
nxlib.nx_setText(ser, nxApp.ID_bi[0], nxApp.ID_bi[1],ini['bi'])
nxlib.nx_setText(ser, nxApp.ID_bd[0], nxApp.ID_bd[1],ini['bd'])
nxlib.nx_setText(ser, nxApp.ID_mturb[0], nxApp.ID_mturb[1],ini['mturb'])
nxlib.nx_setText(ser, nxApp.ID_bturb[0], nxApp.ID_bturb[1],ini['bturb'])

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
        'filename' :filename,
        'googlesh':googlesh,
        'share_email': share_email,
        'google_sheets': google_sheets,
        'duration' :duration,
        'interval' :interval,
        'no_reads' :no_reads,
        'testtype' :testtype,
        'othername':othername,
        'lastip':   lastip
        }

def input_analog():   #inputs from page "analog"
    mu     =   nxlib.nx_getText(ser, nxApp.ID_mu[0], nxApp.ID_mu[1])
    mi     =   nxlib.nx_getText(ser, nxApp.ID_mi[0], nxApp.ID_mi[1])
    md     =   nxlib.nx_getText(ser, nxApp.ID_md[0], nxApp.ID_md[1])
    bu     =   nxlib.nx_getText(ser, nxApp.ID_bu[0], nxApp.ID_bu[1])
    bi     =   nxlib.nx_getText(ser, nxApp.ID_bi[0], nxApp.ID_bi[1])
    bd     =   nxlib.nx_getText(ser, nxApp.ID_bd[0], nxApp.ID_bd[1])
    mturb  =   nxlib.nx_getText(ser, nxApp.ID_mturb[0], nxApp.ID_mturb[1])
    bturb  =   nxlib.nx_getText(ser, nxApp.ID_bturb[0], nxApp.ID_bturb[1])
    return  {
        'mu'   : mu,
        'mi'   : mi,
        'md'   : md,
        'bu'   : bu,
        'bi'   : bi,
        'bd'   : bd,
        'mturb': mturb,
        'bturb': bturb,
         }

def display_analog(data):  #outputs
    #inputs from page "analog"
    nxlib.nx_setText(ser, nxApp.ID_vu[0],   nxApp.ID_vu[1],str(round(data['v_up']*1000)))
    nxlib.nx_setText(ser, nxApp.ID_vi[0],   nxApp.ID_vi[1],str(round(data['v_int']*1000)))
    nxlib.nx_setText(ser, nxApp.ID_vd[0],   nxApp.ID_vd[1],str(round(data['v_down']*1000)))
    nxlib.nx_setText(ser, nxApp.ID_vturb[0],nxApp.ID_vturb[1],str(data['ana_turb']))
    nxlib.nx_setText(ser, nxApp.ID_baru[0], nxApp.ID_baru[1],str(data['bar_up']*1000))
    nxlib.nx_setText(ser, nxApp.ID_bari[0], nxApp.ID_bari[1],str(data['bar_int']*1000))
    nxlib.nx_setText(ser, nxApp.ID_bard[0], nxApp.ID_bard[1],str(data['bar_down']*1000))
    nxlib.nx_setText(ser, nxApp.ID_ntu[0],  nxApp.ID_ntu[1],str(data['turb']))

def display_sensors(data):   #outputs
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d, %H:%M")

    nxlib.nx_setText(ser, nxApp.ID_datetime[0], nxApp.ID_datetime[1],date_time)
    nxlib.nx_setText(ser, nxApp.ID_pu[0], nxApp.ID_pu[1],str(data['mmH2O_up']))
    nxlib.nx_setText(ser, nxApp.ID_pi[0], nxApp.ID_pi[1],str(data['mmH2O_int']))
    nxlib.nx_setText(ser, nxApp.ID_pd[0], nxApp.ID_pd[1],str(data['mmH2O_down']))
    nxlib.nx_setText(ser, nxApp.ID_turb[0], nxApp.ID_turb[1],str(data['turb']))
    nxlib.nx_setText(ser, nxApp.ID_liters[0], nxApp.ID_liters[1],str(data['liters']))
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
nxlib.nx_setValue(ser, nxApp.ID_status[0], nxApp.ID_status[1], 1)  # green flag - ok to proceed

####

def read_display(e_rd): #read and display data in page "analog"
    if inp['testtype'] == "3":  # if HET test is the selection
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
        data=srv.get_data(int(inp['interval']),
                           float(inp['mu']), float(inp['mi']), float(inp['md']),
                           float(inp['bu']), float(inp['bi']), float(inp['bd']),
                           float(inp['mturb']), float(inp['bturb']), zerou, zeroi, zerod, inp['testtype'])
        display_analog(data)
        sleep(int(inp['interval']))
##################

def read_display_write(e_rdw): # read and display data in page "sensors" and write to file
    global stop, con, cur
    #first, check if HET test is selected
    if inp['testtype'] == '3':  # if HET test is the selection
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_pi', 0)
    else:
        nxlib.nx_setcmd_2par(ser, 'vis', 'txt_pi', 1)

    # first write in the inputs.ini file the inputs (that will be the default values next time)
    rw.write_ini(inp['filename'],inp['googlesh'], inp['share_email'], inp['google_sheets'],
                 inp['duration'],inp['interval'], inp['no_reads'],
                 inp['testtype'], inp['othername'],
                 inp['mu'],inp['bu'],inp['mi'],inp['bi'],inp['md'],inp['bd'],
                 inp['mturb'], inp['bturb'], inp['lastip'])

    # obtain the selected worksheet in the google spreadsheet and share it
    export_google = inp['google_sheets']
    if export_google in ['yes','Yes','YES','y','Y','yep'] and gsh.google_creds == True:
        wks = gsh.spreadsheet_worksheet(ssheet_title=inp['googlesh'],
                                        wsheet_title=inp['filename'],
                                        share_email=inp['share_email'])


    e_rdw.wait()
    row = 1
    zero_vol = 0
    while end_rdw.is_set() == False and time.time() < stop+int(inp['interval']):
        if time.time() < stop+int(inp['interval']):
            LED.greenOn()
            e_rdw.wait()
            current = time.time()
            elapsed = current - start# restart thread t_rdw
            elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            autostop =  time.strftime("%H:%M:%S", time.localtime(stop))
            print("write running")
            data=srv.get_data(int(inp['interval']),
                              float(inp['mu']), float(inp['mi']), float(inp['md']),
                              float(inp['bu']), float(inp['bi']), float(inp['bd']),
                              float(inp['mturb']), float(inp['bturb']),
                              zerou, zeroi, zerod, inp['testtype'])
            if current < start+2:   # zero flowrate at start.
                zero_vol= data['liters']
                data['flow'] = 0
            data['liters'] = data['liters']-zero_vol

            # filters readings that are wrong due to overflow of buffer of ADS1115!
            if data['v_up'] != 0 and data['v_int'] != 0 and data['v_down'] != 0 and data['ana_turb'] != 0:
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


            ID_elapsed = nxApp.get_Ids('sensors', 'txt_duration')
            nxlib.nx_setText(ser, ID_elapsed[0], ID_elapsed[1], elapsed)
            ID_autostop = nxApp.get_Ids('sensors', 'txt_autostop')
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

            sleep(float(inp['interval'])-delay)

    # disconnect from database
    cur.close()
    con.close()

    end_rdw.set()
    e_rdw.clear()

    test_end() # morse code sounds to alert for final test

    nxlib.nx_setcmd_1par(ser, 'page', 'credits')
    ip = get_ip_address()
    nxlib.nx_setValue(ser, nxApp.ID_status[0], nxApp.ID_status[1], 1)  # green flag
    nxlib.nx_setText(ser, nxApp.ID_ip[0], nxApp.ID_ip[1], ip)

##################

def input_update(): # update all inputs previous 'analog' and 'sensors' page
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
        inp['testtype'] = '1'
    elif rg == 1:# r1
        inp['testtype'] = '2'
    elif rg == 2:# r2
        inp['testtype'] = '3'
    elif rg == 3:# r3
        inp['testtype'] = '4'
        inp['othername'] = nxlib.nx_getText(ser, nxApp.ID_othername[0], nxApp.ID_othername[1])
    else:
        print('unable to determine test type!')

def detect_touch(e_rd, e_rdw):

    look_touch = 1  # in seconds
    print("detecting serial every {} second(s) ...".format(look_touch))
    global t_rdw
    while True:
        try:
            touch=ser.read_until(EndCom)
            if  hex(touch[0]) == '0x65':  #  touch event. If it's empty don't do nothing
                pageID_touch = touch[1]
                compID_touch = touch[2]
                event_touch = touch[3]
                print("page= {}, component= {}, event= {}".format(pageID_touch,compID_touch,event_touch))

                if (pageID_touch, compID_touch) == (1, 2):  # ip refresh (comp2) in page 1 is pressed
                    ip=get_ip_address()
                    nxlib.nx_setText(ser, nxApp.ID_ip[0], nxApp.ID_ip[1], ip)

                elif (pageID_touch, compID_touch) == (2, 2):  # button set analog sensors (comp2) in page 2 is pressed
                    end_rd.clear()
                    input_update()
                    srv.init(int(inp['interval']),int(inp['no_reads']))

                    t_rd = threading.Thread(target=read_display, name='Read/Display', args=(e_rd,))
                    t_rd.start()

                    sleep(1)  # necessary to allow enough time to start the 1º read of the ads1115 and sensor temp
                    e_rd.set()  # start read_display()

                elif (pageID_touch,compID_touch) == (2,3):  # button start record (comp3) in page 2 is pressed
                    end_rdw.clear()
                    global start, stop, con, cur
                    input_update()
                    srv.init(int(inp['interval']),
                             int(inp['no_reads']))
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
                            "INSERT INTO testinputs (start, test_name, rec_interval, test_type, mu, bu, mi, bi, md, bd, mturb, bturb) "
                            "VALUES (to_timestamp('{}', 'YYYY-MM-DD HH24:MI') , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(datetime.datetime.now()),
                            [inp['filename'], inp['interval'], inp['testtype'],
                             inp['mu'], inp['bu'], inp['mi'], inp['bi'], inp['md'], inp['bd'],
                             inp['mturb'], inp['bturb']])

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
                    if inp['testtype'] != '3':
                        inp['mi'] = nxlib.nx_getText(ser, nxApp.ID_mi[0], nxApp.ID_mi[1])
                        inp['bi'] = nxlib.nx_getText(ser, nxApp.ID_bi[0], nxApp.ID_bi[1])

                    inp['bd'] = nxlib.nx_getText(ser, nxApp.ID_bd[0], nxApp.ID_bd[1])
                    inp['md'] = nxlib.nx_getText(ser, nxApp.ID_md[0], nxApp.ID_md[1])

                    zero = srv.zero_press(float(inp['mu']), float(inp['mi']), float(inp['md']),
                                          float(inp['bu']), float(inp['bi']), float(inp['bd']), inp['testtype'])

                    zerou = zero[0]
                    zeroi = zero[1]
                    zerod = zero[2]

                    if inp['testtype'] == "3":  # if HET test is the selection
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
                    if inp['testtype'] != '3':
                        inp['mi'] = nxlib.nx_getText(ser, nxApp.ID_mi[0],    nxApp.ID_mi[1])
                        inp['bi'] = nxlib.nx_getText(ser, nxApp.ID_bi[0], nxApp.ID_bi[1])
                    inp['md']    = nxlib.nx_getText(ser, nxApp.ID_md[0],    nxApp.ID_md[1])
                    inp['bd']    = nxlib.nx_getText(ser, nxApp.ID_bd[0],    nxApp.ID_bd[1])
                    inp['mturb'] = nxlib.nx_getText(ser, nxApp.ID_mturb[0], nxApp.ID_mturb[1])
                    inp['bturb'] = nxlib.nx_getText(ser, nxApp.ID_bturb[0], nxApp.ID_bturb[1])
                    e_rd.set()

                elif (pageID_touch,compID_touch) == (5,1):  # back button leave analog sensors page (comp 1) in page 5 is pressed
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

                elif (pageID_touch,compID_touch) == (7,1):  # button confirm exit (comp 1) in page 7 is pressed
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