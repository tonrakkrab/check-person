from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_HOST'] = 'migae5o25m2psr4q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'vhqskbgmu3qpnyqa'
app.config['MYSQL_PASSWORD'] = 'peh1p64ucikdulzs'
app.config['MYSQL_DB'] = 'tevm7fxnw6cl3fyr'
 
mysql = MySQL(app)
 
@app.route('/')
def hello_world():
    return 'Hello, world! github'

@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
# for test with local
#app.run(host='localhost', port=5000)
