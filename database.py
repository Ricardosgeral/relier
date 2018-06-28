import psycopg2 as p

#credentials of database in Heroku
Host = 'ec2-23-21-216-174.compute-1.amazonaws.com'
Database = 'dbtnt5r45pnmr4'
User = 'jqgxlpscxtevqg'
Port = '5432'
Password = '1430e8562fbf6d737b0561164e8f88c9d8622e3ff866e434705bd29d9fa2cdf4'
URI = 'postgres://jqgxlpscxtevqg:1430e8562fbf6d737b0561164e8f88c9d8622e3ff866e434705bd29d9fa2cdf4@ec2-23-21-216-174.compute-1.amazonaws.com:5432/dbtnt5r45pnmr4'
Heroku_CLI = 'heroku pg:psql postgresql-transparent-52313 --app relier-dash'

try:
    con = p.connect(dbname=Database, user=User, password=Password, host=Host)
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

