from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)
app.secret_key = 'my-secret-key'
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='movie_theater_storage',
                                         user='root',
                                         password='turbo')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


def get_user_id(username):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='movie_theater_storage',
                                             user='root',
                                             password='turbo')
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    except Error as e:
        print("Error connecting to MySQL database", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def check_login(username, password):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='movie_theater_storage',
                                             user='root',
                                             password='turbo')
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


@app.route('/')
def Landing_Page():
    return render_template('Landing_Page.html')


@app.route('/Login_Page', methods=['GET'])
def login_page():
    return render_template('Login_Page.html')


@app.route('/Login_Page', methods=['POST'])
def login():
    # Get the username and password
    username = request.form['username']
    password = request.form['password']

    # Check if the username and password are correct
    if check_login(username, password):
        # If the login is successful, redirect
        session['user_id'] = get_user_id(username)
        return redirect(url_for('Landing_Page'))
    else:
        # the login is not successful
        error_message = 'Incorrect username or password'
        return render_template('Login_Page.html', error_message=error_message)


@app.route('/Landing_Page')
def home():
    if 'user_id' in session:
        # Highlight 2 User is logged in, display user id welcome
        user_id = session['user_id']
        username = get_username(user_id)
        return f'Welcome back, {username}!'
    else:

        return 'Welcome to the home page!'


@app.route('/Forgot_your_password')
def Forgot_your_password():
    return render_template('Forgot_your_password.html')


@app.route('/Register_account')
def Register_account():
    return render_template('Register_account.html')


def create_user(name, username, email, password):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='movie_theater_storage',
                                             user='root',
                                             password='turbo')
        cursor = connection.cursor()

        # Insert the new user into the database
        query = "INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)"
        values = (name, username, email, password)
        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into users table {}".format(error))

    finally:

        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/Register_account', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the user's registration information from the form
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username is already taken
        #Highlight 3
        if get_user_id(username):
            error_message = 'Username is already taken'
            return render_template('register_account.html', error_message=error_message)

        # If the username is not taken, create a new user in the database
        create_user(name, username, email, password)
        return redirect(url_for('login'))

    else:

        return render_template('register_account.html')


def get_username(user_id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='movie_theater_storage',
                                             user='root',
                                             password='turbo')
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT username FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    except Error as e:
        print("Error connecting to MySQL database", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def is_username_taken(username):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='movie_theater_storage',
                                             user='root',
                                             password='turbo')
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
    except Error as e:
        print("Error connecting to MySQL database", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/book_movie', methods=['POST'])
def book_movie():
    # Highlight 1 Get the movie_id from the form data USE THIS TO CHANGE WHAT MOVIE IS BOOKED
    movie_id = '1'

    user_id = session.get('user_id')

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='movie_theater_storage',
                                             user='root',
                                             password='turbo')

        if connection.is_connected():
            cursor = connection.cursor()

            query = "INSERT INTO booking (user_id, movie_id) VALUES (%s, %s)"
            values = (user_id, movie_id)
            cursor.execute(query, values)

            connection.commit()

            cursor.close()
            connection.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into bookings table {}".format(error))

    finally:

        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect(url_for('Landing_Page'))

@app.route('/Logout')
def logout():
    session.clear()
    return redirect(url_for('Landing_Page'))


if __name__ == '__main__':
    app.run(debug=True)
