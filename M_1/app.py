from flask import Flask , render_template ,url_for , send_from_directory , request , redirect 
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)
app.secret_key ="I_Am_Jesus"


# connecting to database

app.config['MYSQL_PORT'] =3306
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'

# initialize the database & password
mysql = MySQL(app)
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/resume')
def resume():
    return send_from_directory(directory='static' , path='My_Resume.pdf')

@app.route('/register' , methods =['POST','GET'])
def register():
        if request.method == 'POST' :
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            # hash the password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # create cursor object
            cursor= mysql.connection.cursor()

            # insert data to database
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", (username, email, hashed_password))

            # commit the transaction
            mysql.connection.commit()

            # close the connection
            cursor.close()

            return "User registered successfully!"
            
            return redirect (url_for('login'))
        return render_template('register.html')


@app.route('/test_db', methods=['POST','GET'])
def test_db():
     try:
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute('SELECT 1')
          data = cursor.fetchone()
          cursor.close()
          return "the connection is  success_full DB:" + str(data)
     except Exception as e:
          return 'the error is :'+ str(e)


if __name__ == '__main__':
    app.run(debug=True)