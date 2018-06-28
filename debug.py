import psycopg2 as p

#credentials of database in Heroku
Host = 'ec2-23-21-216-174.compute-1.amazonaws.com'
Database = 'dbtnt5r45pnmr4'
User = 'jqgxlpscxtevqg'
Port = '5432'
Password = '1430e8562fbf6d737b0561164e8f88c9d8622e3ff866e434705bd29d9fa2cdf4'
URI = 'postgres://jqgxlpscxtevqg:1430e8562fbf6d737b0561164e8f88c9d8622e3ff866e434705bd29d9fa2cdf4@ec2-23-21-216-174.compute-1.amazonaws.com:5432/dbtnt5r45pnmr4'
Heroku_CLI = 'heroku pg:psql postgresql-transparent-52313 --app relier-dash'


con = p.connect(dbname=Database, user=User, password=Password, host=Host)
cur = con.cursor() # as list


cur.execute("CREATE TABLE testdata (qqcoisa integer, duration interval);")


elapsed = '40:00:24'   #HH:MM:SS
x=20
cur.execute("INSERT INTO testdata(qqcoisa, duration) VALUES({},%s);".format(x),[elapsed,])
con.commit()