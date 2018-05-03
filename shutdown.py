#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import serial
import py3nextion_lib  as nxlib    # simple python3 library to use nextion device

ser = serial.Serial(port='/dev/ttyAMA0', baudrate = 38400,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.15)
#
nxlib.nx_setsys(ser, 'bkcmd',0)     # sets in NEXTION 'no return error/success codes'
nxlib.nx_setcmd_1par(ser,'page',0)  # sends screen to page 0 "not connected"
