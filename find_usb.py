#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import os

def find_dev(path, data_file):
    """Find usb device absolute path.
    Note:
        Also check if data already exists on device (with the given file name
        global variable data_file_exists.
    Args:
        path (str): The path to the dir where the device might be.
        file_name (str): csv file_name where data is to be recorded

    Returns:
        str: Full path (with file name) to the correct usb device.
        if none USB drive is found returns a empty string dev = ''
    """

    global data_file_exists
    data_file_exists = False
    dev = ''

    # Get full path of all devices connected
    dirents = [os.path.join(path, e) for e in os.listdir(path)]

    # Pick first one by default if data don't exists on others
    if dirents:
        dev = dirents[0]

    # Try to find if data file already exists on one root of the device
    for ent in dirents:
        found = False
        for subent in os.listdir(ent):
            if subent == data_file:
                dev = ent
                data_file_exists = True
                found = True
                break
        if found:
            break

    return dev

# x= find_dev('/media/pi', 'test.csv')
# print(x)