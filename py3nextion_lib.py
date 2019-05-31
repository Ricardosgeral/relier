#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import serial
BAUD =38400   # for new monitor please put 9600 and then run nx_setsys(ser, 'bauds', newBAUD)
ser = serial.Serial(
  port='/dev/ttyAMA0',
  baudrate = BAUD,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=0.15)

ser.reset_output_buffer()

EndCom = "\xff\xff\xff"

def nx_setsys(ser, sysvar,value):  # Set system variables. sysvar as text. example: sysvar='dim'
    #Possible commands: 'bkcmd', 'dp', 'dim', 'dims', 'baud', 'bauds', 'ussp', 'thsp', 'thup', 'delay', 'sleep'
    # see instruction set of NEXTION device to see possible values for each system variable
    set = sysvar + '=' + str(value)
    ser.write((set+EndCom).encode('latin-1'))
    return None

def nx_setcmd_0par(ser, command):  #Set operational Commands without parameters
    # Possible commands: 'ref_stop', 'ref_star', 'touch_j' (calibrate), 'com_stop', 'com_start', 'code_c','rest', 'doevents'
    # see instruction set of NEXTION device to know the possible commands and what they do
    ser.write((command+EndCom).encode('latin-1'))
    return None

def nx_setcmd_1par(ser, command, value):  #Set operational Commands with 1 parameters
    # Possible commands: 'page', 'ref'
    # see instruction set of NEXTION device to know the possible commands and what they do
    if value is str:
        set=command +' '+ value  # example 'page initial'
    else:
        set=command +' '+str(value)   #example 'page 1'
    ser.write((set+EndCom).encode('latin-1'))
    return None

def nx_setcmd_2par(ser, command, value1, value2=1):  #Set operational Commands with 2 parameters
    # Possible commands: 'click', 'vis', 'tsw'
    # value2 can only be 0 or 1
    # see instruction set of NEXTION device to know the possible commands and what they do
    if value1 is str:
        set=command + ' ' + str(value1) + ',' + str(value2)   #example 'vis t0,1   show componente t0'
    else:
        set = command + ' ' + str(value1) + ',' + str(value2)  # vis 2,0   hide componentID 2 in current page'
    ser.write((set+EndCom).encode('latin-1'))
    return None

def nx_page(ser):    # reads number of current page show in display
    ser.write(('sendme ' + EndCom).encode('latin-1'))
    page=ser.read_until(EndCom)
    page=str(page)
    page=page.lstrip("b\\'f\\x")
    page=page.rstrip("\\xff\\xff\\xff\\'")
    page = int(page, 16)
    return page

def nx_getText(ser, pageID, componentID):  # Returns the .txt from a component in a page as text
    send = 'get ' + 'p[' + str(pageID) + '].b[' + str(componentID)+']''.txt'
    ser.write((send+EndCom).encode('latin-1'))
    text=ser.read_until(EndCom)
    text = str(text)
    text = text[3:]
    #text = text.lstrip("b\\'p")
    #text = text.rstrip("\\xff\\xff\\xff\\'")
    text = text[:-13]
    return text  # as string"

def nx_getValue(ser, pageID, componentID):  # Returns the .val from a component in a page as text
    send = 'get ' + 'p[' + str(pageID) + '].b[' + str(componentID)+']'+'.val'
    ser.write((send+EndCom).encode('latin-1'))
    value=ser.read_until(EndCom)
    try:
        if hex(value[0]) == '0x71':
            value = value[1]+value[2]*256+value[3]*65536+value[4]*16777216 # little endian
            return value  # as float
    except:
        pass

def nx_setText(ser, pageID, componentID, text):  # writes the text in the text component atribute .txt
    text = 'p[' + str(pageID) + '].b[' + str(componentID)+']''.txt="' + text + '"'
    ser.write((text+EndCom).encode('latin-1'))
    return None

def nx_setValue(ser, pageID, componentID, value):  # writes the value in the number component atribute .val
    value_str = 'p[' + str(pageID) + '].b[' + str(componentID)+']''.val=' + str(value)  # test here the "'"
    ser.write((value_str+EndCom).encode('latin-1'))
    return None


####### examples of usage

#nx_setsys(ser, 'bauds', BAUD)  # set default baud

#nx_setsys(ser, 'dim',80)                    # sets backlight of device 1 to 100
#nx_setsys(ser, 'bkcmd',0)     # avoids receiving bytes used in debugging

#nx_setcmd_1par(ser, 'page','initial')       # go to page named 'initial'
#nx_setcmd_0par(ser, 'rest')                 # reboot the device

#nx_getValue(ser, 2,3)
#nx_setText(ser, 2,3,'3000')
#nx_setValue(ser, pageID=4,componentID=3,80)