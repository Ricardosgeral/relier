#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import pygsheets
import pandas as pd

# get signed credentials
try:
    gc = pygsheets.authorize(service_file='service_creds_copy.json') # remove the _copy part
    initial_rows = 1000  # default number of rows of the worksheet
    initial_colmn = 15  # default number of columns
    google_creds = True
except:
    print('Problem: Google signed credentials')
    google_creds = False

def spreadsheet_worksheet(ssheet_title, wsheet_title, share_email):
    # get spredsheet instance
    list_of_ssheets = gc.list_ssheets()  # gets all the available sheets in the account of the service_creds.jon
    ssheet_exists = False
    for ssheet in list_of_ssheets:
        if ssheet['name'] == ssheet_title:
            ssheet_exists = True
    if ssheet_exists == True:                   # if sheet exists
        sh = gc.open(ssheet_title)              # open it
    else:                                       # if sheet does not exists
        sh = gc.create(ssheet_title)            # create it

    sh.share(share_email, role='writer')        # share it to the provided email

    wsheet_exists = False
    try:
        sh.worksheets(sheet_property='title',value= wsheet_title)
        wsheet_exists = True
    except:
        pass

    if wsheet_exists == True:
        wks = sh.worksheet(property='title', value= wsheet_title)
        wks.clear()
    else:
        wks = sh.add_worksheet(title=wsheet_title, rows=str(initial_rows), cols=str(initial_colmn))

    #cell instance
    a1 = wks.cell('A1')
    a1.text_format['bold'] = True    # set headers to bold
    a1.update()
    # Getting a Range object
    rng = wks.get_values('A1', 'I1', returnas='range')
    rng.apply_format(a1)  # set format of a1 to all cells in the range rng
    return wks

def write_gsh(data, row, wks):
    global initial_rows
    fieldnames = ['date', 'time',
                  # 'v_up', 'v_int', 'v_down',
                  # 'bar_up', 'bar_int', 'bar_down',
                  'mmH2O_up', 'mmH2O_int', 'mmH2O_down',
                  'ana_turb', 'ntu_turb', 'flow', 'liters',
                  # 'water_temp', 'air_temp', 'air_pressure', 'air_humidity'
                  ]

    df = pd.DataFrame(columns=fieldnames)
    # Create a row
    df.loc[-1]=[data['date'], data['time'],
                 #data['v_up'], data['v_int'], data['v_down'],
                 #data['bar_up'], data['bar_int'], data['bar_down'],
                 data['mmH2O_up'], data['mmH2O_int'], data['mmH2O_down'],
                 data['ana_turb'], data['ntu_turb'], data['flow'], data['liters'],
                 #data['water_temp', data['air_temp', data['air_pressure', data['air_humidity'
                ]
    df.index = df.index + 1

    #update the first sheet with df
    if row == 1:
        wks.set_dataframe(df,(row,1),copy_head=True)
    else:
        wks.set_dataframe(df, (row + 1, 1), copy_head=False)
        if row == initial_rows-3: # when max number of rows is being reached
            wks.add_rows(1000)      #adds another 1000 rows
            initial_rows += 1000    #new number of rows