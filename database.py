import psycopg2 as p

#credentials of database in Heroku  # to obtain it $ heroku config, or look in https://data.heroku.com/  -> database -> settings -> Database Credentials -> URI
DATABASE_URL = 'postgres://wvqemnhwnijypm:7b08a0b8700d1d6850a802c0eb61649999e8ee11bec7be91c8623b99aaac80df@ec2-54-163-228-190.compute-1.amazonaws.com:5432/de93scsb82pcp1'
import urllib.parse as urlparse
import os

url = urlparse.urlparse(DATABASE_URL)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

def connect_db():
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
        print('Database table for results already exists! Data will be cleared!')
        cur.execute('rollback;')

    #create a table to parse test relevant inputs to  heroku app
    try:
        cur.execute("CREATE TABLE testinputs (start timestamp, test_name text, rec_interval integer, test_type integer, "
                    "mu float, bu float,mi float, bi float,md float, bd float,mturb float, bturb float);")
        con.commit()
        print('Database table for test inputs created!')
    except:
        print('Database table for inputs already exists! Data will be cleared!')
        cur.execute('rollback;')

    return con, cur

