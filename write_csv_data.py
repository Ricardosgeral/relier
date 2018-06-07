#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

from find_usb import find_dev
from csv import DictWriter, DictReader # write csv data file
import os
import rw_ini as rw


def write_data(data, data_file):
    """Write data in the file (usb or if not available in SD card).

    Args:
        data (dict): The dict containing the data for each parameter (result dict from function get_data()).
    """

    path = find_dev('/media/pi/', data_file)
    fieldnames = [
                    'date',
                    'time',
                    'v_up',     # V
                    'v_int',    # V
                    'v_down',   # V
                    'bar_up',   # bar
                    'bar_int',  # bar
                    'bar_down', # bar
                    'mmH2O_up',
                    'mmH2O_int',
                    'mmH2O_down',
                    'ana_turb', # analog number
                    'ntu_turb',
                    'flow',
                    'liters',
                    'water_temp',
                    'air_temp',
                    'air_pressure',
                    'air_humidity',
                ]

    #Put csv extention if not present
    if data_file[-4:] != '.csv':
        csv_file= data_file + '.csv'
    else:
        csv_file = data_file

    if path == '':
        # If there is no storage device, write on disk (RPi sd card) in /srv/sensors
        # don't forget to do 1st:   sudo mkdir /srv/sensors
        #                           sudo chmod - R 777 / srv / sensors

        path = os.path.join('/srv/EROSTESTS', csv_file)  #create first the /srv/EROSTESTS/
        file_exists = os.path.isfile(path)  # sets to TRUE if file exists otherwise FALSE

        rw.write_ini_path(path)
        os.chmod(path, 0o777)

        with open(path, 'a', newline='') as f: # if the file exists data will be added below after a black line
            writer = DictWriter(f, fieldnames)
            if not file_exists:
                writer.writeheader()    # file doesn't exist yet, write a header
            writer.writerow(data)       #writes the data in a new blank line
    else:
        # If storage USB device available
        # Create the full path to the file on the device
        path = os.path.join(path, csv_file)
        file_exists = os.path.isfile(path)
        rw.write_ini_path(path)
        os.chmod(path, 0o777)

        with open(path, 'a', newline='') as f:# if the file exists data will be added below after a black line
            writer = DictWriter(f, fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
