#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import configparser
config = configparser.ConfigParser()
config.read("inputs.ini")
config.sections()

def read_ini(): ###read the init file
    filename    = config['settings']['filename']
    googlesh    = config['settings']['googlesh']
    share_email = config['settings']['share_email']
    google_sheets   = config['settings']['google_sheets']
    duration    = config['settings']['duration']
    interval    = config['settings']['interval']
    no_reads    = config['settings']['no_reads']
    testtype    = config['testtype']['test_type']
    othername   = config['testtype']['othername']
    mu          = config['analog']['mu']
    bu          = config['analog']['bu']
    mi          = config['analog']['mi']
    bi          = config['analog']['bi']
    md          = config['analog']['md']
    bd          = config['analog']['bd']
    flowmeter_type  = config['flowmeter']['flowmeter_type']
    cf          = config['flowmeter']['cf']


    return {'filename': filename,
            'googlesh': googlesh,
            'share_email': share_email,
            'google_sheets': google_sheets,
            'duration' : duration,
            'interval' : interval,
            'no_reads' : no_reads,
            'test_type' : testtype,    # 1 -FLET; 2 - CFET; 3- HET; 4 - Other
            'othername': othername,   # if testtype = 4
            'mu': mu,
            'bu': bu,
            'mi': mi,
            'bi': bi,
            'md': md,
            'bd': bd,
            'flowmeter_type': flowmeter_type,
            'cf': cf,
            }

#write in the ini file
def write_ini(filename, googlesh, share_email, google_sheets, duration, interval, no_reads,
              testtype, othername,
              mu, bu, mi, bi, md, bd, flowmeter_type, cf, lastip):

    config['settings'] = {'filename': filename,
                          'googlesh': googlesh,
                          'share_email': share_email,
                          'google_sheets': google_sheets,
                          'duration': duration,
                          'interval': interval,
                          'no_reads': no_reads,
                          }

    config['testtype'] = {'test_type': testtype,    # 1 - FLET; 2 - CFET; 3 - HET; 4 - Other
                         'othername': othername    # if testtype = 4
                          }
    config['sensors'] = {'mu':mu,
                        'bu': bu,
                        'mi': mi,
                        'bi': bi,
                        'md': md,
                        'bd': bd,
                        }

    config['ip'] = {'lastip': lastip}

    config['flowmeter'] = {'flowmeter_type':flowmeter_type,  #1 - Eletromagnetic; 2 - turbine flowmeter
                           'cf': cf
                           }


    with open('inputs.ini', 'w') as configfile:
        config.write(configfile)


#write in the ini file only the pathname (useful for dash)
def write_ini_path(path):

    config['path'] = {'lastpath': path}
    with open('inputs.ini', 'w') as configfile:
        config.write(configfile)
