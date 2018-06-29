import psycopg2 as p

#credentials of database in Heroku  # can obtain it from $ heroku config
DATABASE_URL = 'postgres://thdhsoxbktdpux:93abf552793c4d495574746f31eefe83af6935549860f618394d7ba66e657482@ec2-23-23-245-89.compute-1.amazonaws.com:5432/d32aeuhq8264kf'

import urllib.parse as urlparse
import os

url = urlparse.urlparse(DATABASE_URL)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

try:
    con = p.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port)

    cur = con.cursor() # as list
except:
    print('No connection with Heroku database! DB is local and NO live data streaming!')
    con= p.connect(dbname='testdata_local', user='relier', password='relier-dash', host='localhost')
    cur= con.cursor() # as list

#create table (only first time) with the data results
try:
    cur.execute("CREATE TABLE testdata ("
                 "id serial PRIMARY KEY, "
                 "date_time timestamp,"
                 "duration interval, "
                 "mmH2O_up integer, "
                 "mmH2O_int integer, "
                 "mmH2O_down integer, "
                 "turb float, "
                 "flow float, "
                 "volume integer);")
    con.commit()
    print('Database table for test results created!')
except:
    print('Database table for results already exists! Cleared!')
    cur.execute('rollback;')

#create a table to parse test relevant inputs to  heroku app
try:
    cur.execute("CREATE TABLE testinputs (start timestamp, test_name varchar, rec_interval integer, test_type integer, "
                "mu float, bu float,mi float, bi float,md float, bd float,mturb float, bturb float);")
    con.commit()
    print('Database table for test inputs created!')
except:
    print('Database table for inputs already exists! Cleared!')
    cur.execute('rollback;')



#close connection
def close_db():
    cur.close()
    con.close()

