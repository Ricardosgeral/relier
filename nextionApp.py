#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

# set all the components
class NextionApp:

    # initialization of the components used in device

    def __init__(self):
        self.pages = [
            {'id': 1, 'name': 'credits',
             'components': [
                 {'id': 1, 'type': 'button', 'name': 'b0'},
                 {'id': 2, 'type': 'text',   'name': 'txt_ip'},
                 {'id': 3, 'type': 'dualbuttom', 'name': 'txt_status'}
             ]
             },
            {'id': 2, 'name': 'initial',
             'components': [
                 {'id': 1, 'type': 'button', 'name': 'bt_settings'},
                 {'id': 2, 'type': 'button', 'name': 'bt_sensors'},
                 {'id': 3, 'type': 'button', 'name': 'bt_start'},
             ]
             },
            {'id': 3, 'name': 'settings',
             'components': [
                 {'id': 1, 'type': 'text',   'name': 'txt_filename'},
                 {'id': 2, 'type': 'text',   'name': 'txt_googlesh'},
                 {'id': 8, 'type': 'text',   'name': 'txt_email'},
                 {'id': 9, 'type': 'variable', 'name': 'chk_google'},  # check button to export to google sheets
                 {'id': 3, 'type': 'text',   'name': 'txt_duration'},
                 {'id': 4, 'type': 'text',   'name': 'txt_interval'},
                 {'id': 5, 'type': 'text',   'name': 'txt_no_reads'},
                 {'id': 6, 'type': 'button', 'name': 'bt_back'}, # back button
                 {'id': 7, 'type': 'button', 'name': 'bt_type'}, # Test type selection
             ]
             },
            {'id': 4, 'name': 'testType',
             'components': [
                 {'id': 8,  'type': 'variable',     'name': 'rg'},  # variable that determines the testtype 0 to 3
                 {'id': 12, 'type': 'text',         'name': 'txt_othername'},  # name of the test in OTHER
             ]
             },
            {'id': 5, 'name': 'sensors',
             'components': [
                 {'id': 1,  'type': 'button', 'name': 'bt_back'},  # back button
                 {'id': 2,  'type': 'button', 'name': 'bt_home'},  # back home
                 {'id': 3,  'type': 'button', 'name': 'bt_zero'},  # zero the pressures
                 {'id': 4,  'type': 'button', 'name': 'bt_zero'},  # refresh calibration
                 {'id': 5,  'type': 'text',   'name': 'txt_vu'},
                 {'id': 6,  'type': 'text',   'name': 'txt_vi'},
                 {'id': 7,  'type': 'text',   'name': 'txt_vd'},
                 {'id': 8,  'type': 'text',   'name': 'txt_anaturb'},
                 {'id': 9,  'type': 'text',   'name': 'txt_baru'},
                 {'id': 10, 'type': 'text',   'name': 'txt_bari'},
                 {'id': 11, 'type': 'text',   'name': 'txt_bard'},
                 {'id': 12, 'type': 'text',   'name': 'txt_ntu'},
                 {'id': 13, 'type': 'text',   'name': 'txt_mu'},
                 {'id': 14, 'type': 'text',   'name': 'txt_mi'},
                 {'id': 15, 'type': 'text',   'name': 'txt_md'},
                 {'id': 16, 'type': 'text',   'name': 'txt_bu'},
                 {'id': 17, 'type': 'text',   'name': 'txt_bi'},
                 {'id': 18, 'type': 'text',   'name': 'txt_bd'},
                 {'id': 19, 'type': 'button', 'name': 'bt_flowtype'},
                 {'id': 20, 'type': 'text',   'name': 'txt_flowrate'},
             ]
             },

            {'id': 6, 'name': 'flowtype',
             'components': [
                 {'id': 7, 'type': 'text',     'name': 'txt_cf'},
                 {'id': 2, 'type': 'button',   'name': 'dual_bt'},
             ]
             },

            {'id': 7, 'name': 'timelapse',
             'components': [
                 {'id': 1, 'type': 'checkbox', 'name': 'c0'},  # take time-lapse
                 {'id': 2, 'type': 'checkbox', 'name': 'c1'},  # make video
                 {'id': 3, 'type': 'checkbox', 'name': 'c2'},  # delete images after movie
                 {'id': 7, 'type': 'text', 'name': 'txt_freq'},  # definition of the frequency fps
                 {'id': 8, 'type': 'text', 'name': 'txt_max_dur'},  # definition of the maximum duration of the video
                 {'id': 9, 'type': 'text', 'name': 'txt_ratio'},  # definition of the maximum duration of the video
                 {'id': 10, 'type': 'text', 'name': 'txt_vid_dur'},  # duration of video
                 {'id': 11, 'type': 'text', 'name': 'txt_test_dur'},  # duration of test
                 {'id': 12, 'type': 'variable', 'name': 'rg1'},  # variable that determines the frequency of images / maximum duration of video
                 {'id': 13, 'type': 'toucharea', 'name': 'm0'},

             ]
             },

            {'id': 8, 'name': 'record',
             'components': [
                 {'id': 1,  'type': 'button', 'name': 'bt_start'},  # zero the pressures
                 {'id': 2,  'type': 'text',   'name': 'txt_datetime'},
                 {'id': 3,  'type': 'text',   'name': 'txt_duration'},
                 {'id': 4,  'type': 'text',   'name': 'txt_pu'},
                 {'id': 5,  'type': 'text',   'name': 'txt_pi'},
                 {'id': 6,  'type': 'text',   'name': 'txt_pd'},
                 {'id': 7,  'type': 'text',   'name': 'txt_flow'},
                 {'id': 8,  'type': 'text',   'name': 'txt_liters'},
                 {'id': 9,  'type': 'text',   'name': 'txt_turb'},
                 {'id': 10, 'type': 'text',   'name': 'txt_tw'},
                 {'id': 11, 'type': 'text',   'name': 'txt_ta'},
                 {'id': 12, 'type': 'text',   'name': 'txt_hd'},
                 {'id': 13, 'type': 'text',   'name': 'txt_pa'},
                 {'id': 14, 'type': 'text',   'name': 'txt_autostop'},

             ]
             },
            {'id': 9, 'name': 'stop_confirm',
             'components': [
                 {'id': 1, 'type': 'button', 'name': 'bt_end'},  # zero the pressures
                 {'id': 2, 'type': 'button', 'name': 'bt_continue'},  # back button
             ]
             }
        ]

##  function get page ID and component ID, based on the names of page and component in the class
def get_Ids(pageName, compName):
   for element in NextionApp().pages:
       if element['name'] == pageName:
           pag_id = element['id']
           for component in element['components']:
               if component['name'] == compName:
                   comp_id = component['id']
                   return pag_id, comp_id


# ###INITIAL INPUTS from NEXTION by name
#credits page
ID_ip = get_Ids('credits', 'txt_ip')
ID_status = get_Ids('credits', 'txt_status')

# settings page
ID_filename    = get_Ids('settings', 'txt_filename')
ID_googlesh    = get_Ids('settings', 'txt_googlesh')
ID_share_email = get_Ids('settings', 'txt_email')
ID_google_sheets = get_Ids('settings', 'chk_google')
ID_duration    = get_Ids('settings', 'txt_duration')
ID_interval    = get_Ids('settings', 'txt_interval')
ID_no_reads    = get_Ids('settings', 'txt_no_reads')

# "testType" page
ID_rg        = get_Ids('testType', 'rg')  # variable that defines the test type
ID_othername = get_Ids('testType', 'txt_othername')  # get Ids of 'txt_other' comp

# "sensors" page
ID_mu    = get_Ids('sensors', 'txt_mu')
ID_mi    = get_Ids('sensors', 'txt_mi')
ID_md    = get_Ids('sensors', 'txt_md')
ID_bu    = get_Ids('sensors', 'txt_bu')
ID_bi    = get_Ids('sensors', 'txt_bi')
ID_bd    = get_Ids('sensors', 'txt_bd')

ID_vu    = get_Ids('sensors', 'txt_vu')
ID_vi    = get_Ids('sensors', 'txt_vi')
ID_vd    = get_Ids('sensors', 'txt_vd')
ID_vturb = get_Ids('sensors', 'txt_anaturb')
ID_baru  = get_Ids('sensors', 'txt_baru')
ID_bari  = get_Ids('sensors', 'txt_bari')
ID_bard  = get_Ids('sensors', 'txt_bard')
ID_ntu   = get_Ids('sensors', 'txt_ntu')
ID_flowrate   = get_Ids('sensors', 'txt_flowrate')

# "flowtype" page

ID_flowmeter = get_Ids('flowtype', 'dual_bt')
ID_cf = get_Ids('flowtype', 'txt_cf')

# "timelapse" page

ID_doTimeLapse    = get_Ids('timelapse', 'c0')
ID_doVideo        = get_Ids('timelapse', 'c1')
ID_delImages      = get_Ids('timelapse', 'c2')
ID_freqPics       = get_Ids('timelapse', 'txt_freq')
ID_maxVideoDur    = get_Ids('timelapse', 'txt_max_dur')
ID_ratioVideoTest = get_Ids('timelapse', 'txt_ratio')
ID_videoDur       = get_Ids('timelapse', 'txt_vid_dur')
ID_testDur        = get_Ids('timelapse', 'txt_test_dur')
ID_choiceVideoDur = get_Ids('timelapse', 'rg1')

# "record" page
ID_datetime = get_Ids('record', 'txt_datetime')
ID_pu       = get_Ids('record', 'txt_pu')
ID_pi       = get_Ids('record', 'txt_pi')
ID_pd       = get_Ids('record', 'txt_pd')
ID_turb     = get_Ids('record', 'txt_turb')
ID_tw       = get_Ids('record', 'txt_tw')
ID_flow     = get_Ids('record', 'txt_flow')
ID_liters   = get_Ids('record', 'txt_liters')
ID_ta       = get_Ids('record', 'txt_ta')
ID_hd       = get_Ids('record', 'txt_hd')
ID_pa       = get_Ids('record', 'txt_pa')