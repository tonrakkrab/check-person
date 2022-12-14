# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 
app = Flask(__name__)
 
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'migae5o25m2psr4q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'vhqskbgmu3qpnyqa'
app.config['MYSQL_PASSWORD'] = 'peh1p64ucikdulzs'
app.config['MYSQL_DB'] = 'tevm7fxnw6cl3fyr'
 
mysql = MySQL(app)


@app.route('/')
def hello_world():
    #return 'Hello, world!'
    return render_template("index.html")


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password, ))
        users = cursor.fetchone()
        if users:
            session['loggedin'] = True
            session['user_id'] = users['user_id']
            session['username'] = users['username']
            msg = 'Logged in successfully !'
            return render_template('main.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('user_id', None)
   session.pop('username', None)
   return redirect(url_for('login'))


@app.route('/user')
#@login_required
def user():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return render_template("user.html", users = users)        
    return redirect(url_for('login'))

@app.route("/user_view", methods =['GET', 'POST'])
def user_view():
    if 'loggedin' in session:
        viewUserId = request.args.get('userid')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (viewUserId, ))
        user = cursor.fetchone()   
        return render_template("user_view.html", user = user)
    return redirect(url_for('login'))

@app.route("/user_edit", methods =['GET', 'POST'])
def user_edit():
    msg = ''    
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (editUserId, ))
        editUser = cursor.fetchone()
        # if request.method == 'POST' and 'username' in request.form and 'user_id' in request.form and 'role' in request.form and 'country' in request.form :
        if request.method == 'POST' and 'username' in request.form and 'user_id' in request.form :
            userName = request.form['username']   
            # role = request.form['role']
            # country = request.form['country']            
            userId = request.form['user_id']
            if not re.match(r'[A-Za-z0-9]+', userName):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE users SET username =%s WHERE user_id =%s', (userName, userId) )
                mysql.connection.commit()
                msg = 'User updated !'
                return redirect(url_for('user'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'        
        return render_template("user_edit.html", msg = msg, editUser = editUser)

    return redirect(url_for('login'))

@app.route("/user_delete")
def user_delete():
    if 'loggedin' in session:
        return render_template("user.html")
    return redirect(url_for('login'))


@app.route('/person')
#@login_required
def person():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM persons')
        sql = 'SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id'
        cursor.execute(sql)        
        persons = cursor.fetchall()
        return render_template("person.html", persons = persons)        
    return redirect(url_for('login'))

@app.route("/person_view", methods =['GET', 'POST'])
def person_view():
    if 'loggedin' in session:
        viewPersonId = request.args.get('personid')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM persons WHERE person_id = %s', (viewPersonId, ))
        cursor.execute('SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id WHERE person_id = %s', (viewPersonId, ))
        person = cursor.fetchone()   
        return render_template("person_view.html", person = person)
    return redirect(url_for('login'))


@app.route("/person_edit", methods =['GET', 'POST'])
def person_edit():
    msg = ''    
    if 'loggedin' in session:
        editPersonId = request.args.get('personid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM persons WHERE person_id = %s', (editPersonId, ))
        cursor.execute('SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id WHERE person_id = %s', (editPersonId, ))
        editPerson = cursor.fetchone()
        # if request.method == 'POST' and 'username' in request.form and 'user_id' in request.form and 'role' in request.form and 'country' in request.form :
        if request.method == 'POST' and 'firstname_th' in request.form and 'person_id' in request.form :
                        
            personId = request.form['person_id']

            identify = request.form['identify']
            ID_card_photo_path = request.form['ID_card_photo_path']
            firstname_th = request.form['firstname_th']
            lastname_th = request.form['lastname_th']
            telephone_number = request.form['telephone_number']

            trip_type_id = request.form['trip_type']

            #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute('SELECT * FROM persons WHERE email = % s', (email, ))
            # account = cursor.fetchone()
            # if account:
            #     mesage = 'User already exists !'
            # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            #     mesage = 'Invalid email address !'
            # elif not firstname or not lastname or not email:
            #     mesage = 'Please fill out the form !'
            # else:

            # if not re.match(r'[A-Za-z0-9]+', firstname_th):
            #     msg = 'name must contain only characters and numbers !'
            # else:
            cursor.execute('UPDATE persons SET identify =%s , ID_card_photo_path =%s , firstname_th =%s , lastname_th =%s ,telephone_number =%s ,  trip_type_id =%s WHERE person_id =%s', (identify, ID_card_photo_path, firstname_th, lastname_th ,telephone_number, trip_type_id,personId))
            mysql.connection.commit()
            msg = 'User updated !'
            return redirect(url_for('person'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'

        cursor.execute("SELECT * FROM trip_types order by trip_type_id asc")
        tripTypesList = cursor.fetchall()

        cursor.execute("SELECT * FROM provinces order by id asc")
        provincesList = cursor.fetchall()

        cursor.execute("SELECT * FROM amphures order by id asc")
        amphuresList = cursor.fetchall()

        cursor.execute("SELECT * FROM districts order by id asc")
        districtsList = cursor.fetchall() 

        return render_template("person_edit.html", msg = msg, editPerson = editPerson, tripTypesList = tripTypesList, provincesList = provincesList, amphuresList = amphuresList, districtsList = districtsList)
        
    return redirect(url_for('login'))


@app.route('/person_add', methods =['GET', 'POST'])
def person_add():
    msg = ''    

    if request.method == 'POST' and 'identify' in request.form and 'ID_card_photo_path' in request.form and 'firstname_th' in request.form and 'lastname_th' in request.form and 'telephone_number' in request.form and 'trip_type' in request.form :
        identify = request.form['identify']
        ID_card_photo_path = request.form['ID_card_photo_path']
        firstname_th = request.form['firstname_th']
        lastname_th = request.form['lastname_th']
        telephone_number = request.form['telephone_number']

        trip_type_id = request.form['trip_type']

        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM persons WHERE email = % s', (email, ))
        # account = cursor.fetchone()
        # if account:
        #     mesage = 'User already exists !'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     mesage = 'Invalid email address !'
        # elif not firstname or not lastname or not email:
        #     mesage = 'Please fill out the form !'
        # else:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # sql = 'INSERT INTO persons (identify, ID_card_photo_path, firstname_th, lastname_th, telephone_number, trip_type_id) VALUES (NULL, %s, %s, %s, %s, %s, %s)'
        # value = (identify, ID_card_photo_path, firstname_th, lastname_th, telephone_number, trip_type_id)        
        # cursor.execute(sql, value)
        cursor.execute('INSERT INTO persons (identify, ID_card_photo_path, firstname_th, lastname_th, telephone_number, trip_type_id) VALUES (%s, %s, %s, %s, %s, %s)', (identify, ID_card_photo_path, firstname_th, lastname_th, telephone_number, trip_type_id))                
        
        mysql.connection.commit()
        msg = 'New person created!'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT * FROM trip_types order by trip_type_id asc")
        tripTypesList = cursor.fetchall()

        cursor.execute("SELECT * FROM provinces order by id asc")
        provincesList = cursor.fetchall()

        cursor.execute("SELECT * FROM amphures order by id asc")
        amphuresList = cursor.fetchall()

        cursor.execute("SELECT * FROM districts order by id asc")
        districtsList = cursor.fetchall() 

        return render_template('person_add.html', msg = msg, tripTypesList = tripTypesList, provincesList = provincesList, amphuresList = amphuresList, districtsList = districtsList)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id')
    persons = cursor.fetchall()

    return render_template('person.html', msg = msg, persons = persons)


@app.route("/person_delete")
def person_delete():
    if 'loggedin' in session:
        return render_template("person.html")
    return redirect(url_for('login'))


# (C)
@app.route("/person_search", methods=["GET", "POST"])
def person_search():
  # (C1) SEARCH FOR PERSONS
  if request.method == "POST":
    data = dict(request.form)
    persons = getperson(data["search1"],data["search2"])
  else:
    persons = []
 
  # (C2) RENDER HTML PAGE
  return render_template("person.html", persons=persons)

# (B) HELPER FUNCTION - SEARCH PERSONS
def getperson(search1,search2):
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id WHERE firstname_th LIKE %s AND lastname_th LIKE %s', ('%'+search1+'%', '%'+search2+'%'))
  results = cursor.fetchall()  
  return results


if __name__ == "__main__":
    app.run(host ="localhost", port = int("5000"))