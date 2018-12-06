import psycopg2

#credentials of database in Heroku  # to obtain it $ heroku config, or look in https://data.heroku.com/  -> database -> settings -> Database Credentials -> URI
DATABASE_URL = 'postgres://ejpdnwfhlrfilh:986d5c4d2782d8c39904f51fcf9d5e1db9809473fa20e3fc05552792f36ea847@ec2-54-204-40-248.compute-1.amazonaws.com:5432/dekc4e7p0jmc28'

import urllib.parse as urlparse

url = urlparse.urlparse(DATABASE_URL)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

def connect_db():
    try:
        con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port)

        cur = con.cursor() # as list
    except:
        print('No connection with Heroku database! DB is local and NO live data streaming!')
        con= psycopg2.connect(dbname='testdata_local', user='relier', password='relier-dash', host='localhost')
        cur= con.cursor() # as list

    #create table (only first time) with the data results
    try:
        #cur.execute("SET timezone = 'Europe/Lisbon Portugal';") # https://www.postgresql.org/docs/8.1/static/datetime-keywords.html
        cur.execute("CREATE TABLE testdata ("
                     "id serial PRIMARY KEY, "
                     "date_time timestamptz,"
                     "duration interval, "
                     "mmH2O_up integer, "
                     "mmH2O_int integer, "
                     "mmH2O_down integer, "
                     "turb float, "
                     "flow float, "
                     "volume float);")
        con.commit()
        print('Database table for test results created!')
    except:
        print('Database table for results already exists! Data will be cleared!')
        cur.execute('rollback;')

    #create a table to parse test relevant inputs to  heroku app
    try:
        cur.execute("CREATE TABLE testinputs ("
                    "start timestamptz,"
                    "test_name text,"
                    "rec_interval integer,"
                    "test_type integer,"
                    "mu float,"
                    "bu float,"
                    "mi float,"
                    "bi float,"
                    "md float,"
                    "bd float);")
        con.commit()
        print('Database table for test inputs created!')
    except:
        print('Database table for inputs already exists! Data will be cleared!')
        cur.execute('rollback;')

    return con, cur

