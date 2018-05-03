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
    testtype    = config['testtype']['testtype']
    othername   = config['testtype']['othername']
    mu          = config['analog']['mu']
    bu          = config['analog']['bu']
    mi          = config['analog']['mi']
    bi          = config['analog']['bi']
    md          = config['analog']['md']
    bd          = config['analog']['bd']
    mturb       = config['analog']['mturb']
    bturb       = config['analog']['bturb']

    return {'filename': filename,
            'googlesh': googlesh,
            'share_email': share_email,
            'google_sheets': google_sheets,
            'duration' : duration,
            'interval' : interval,
            'no_reads' : no_reads,
            'testtype' : testtype,    # 1 -FLET; 2 - CFET; 3- HET; 4 - Other
            'othername': othername,   # if testtype = 4
            'mu': mu,
            'bu': bu,
            'mi': mi,
            'bi': bi,
            'md': md,
            'bd': bd,
            'mturb': mturb,
            'bturb': bturb,
            }

#write in the ini file
def write_ini(filename, googlesh, share_email, google_sheets, duration, interval, no_reads,
              testtype, othername,
              mu, bu, mi, bi, md, bd, mturb, bturb,lastip):

    config['settings'] = {'filename': filename,
                          'googlesh': googlesh,
                          'share_email': share_email,
                          'google_sheets': google_sheets,
                          'duration': duration,
                          'interval': interval,
                          'no_reads': no_reads,
                          }

    config['testtype'] = {'testtype': testtype,    # 1 - FLET; 2 - CFET; 3 - HET; 4 - Other
                         'othername': othername    # if testtype = 4
                          }
    config['analog'] = {'mu':mu,
                        'bu': bu,
                        'mi': mi,
                        'bi': bi,
                        'md': md,
                        'bd': bd,
                        'mturb': mturb,
                        'bturb': bturb,
                        }

    config['other'] = {'lastip': lastip}

    with open('inputs.ini', 'w') as configfile:
        config.write(configfile)