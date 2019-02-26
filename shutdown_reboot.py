#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import py3nextion_lib  as nxlib    # simple python3 library to use nextion device

ser = nxlib.ser

def reboot_pi():
    nxlib.nx_setsys(ser, 'bkcmd',0)     # sets in NEXTION 'no return error/success codes'
    nxlib.nx_setcmd_1par(ser,'page',0)  # sends screen to page 0 "reboot"

def shutdown_pi():
    nxlib.nx_setsys(ser, 'bkcmd',0)     # sets in NEXTION 'no return error/success codes'
    nxlib.nx_setcmd_1par(ser,'page',11)  # sends screen to page 9 "shutdown"
