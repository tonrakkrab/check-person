from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'migae5o25m2psr4q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'vhqskbgmu3qpnyqa'
app.config['MYSQL_PASSWORD'] = 'peh1p64ucikdulzs'
app.config['MYSQL_DB'] = 'tevm7fxnw6cl3fyr'
 
mysql = MySQL(app)

#Creating a connection cursor
cursor = mysql.connection.cursor()
 
#Executing SQL Statements
#cursor.execute(''' CREATE TABLE table_name(field1, field2...) ''')
#cursor.execute(''' INSERT INTO table_name VALUES(v1,v2...) ''')
#cursor.execute(''' DELETE FROM table_name WHERE condition ''')
cursor.execute(''' CREATE TABLE info_table2(name varchar(200), age int) ''')
 
#Saving the Actions performed on the DB
mysql.connection.commit()
 
#Closing the cursor
cursor.close()