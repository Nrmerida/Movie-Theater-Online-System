from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import random
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
    if 'user_id' in session:
        #Highlight 1 User is logged in, display popup
        user_id = session['user_id']
        username = get_username(user_id)
        return render_template('Landing_Page.html') + render_template('popup_for_login.html', username=username)
    else:
        # User is not logged in, display landing page
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
        return render_template('Login_Page.html') + render_template('Login_error_popup.html')


@app.route('/Forgot_your_password')
def Forgot_your_password():
    return render_template('Forgot_your_password.html')


@app.route('/Register_account')
def Register_account():
    return render_template('Register_account.html')

@app.route('/Movie_details')
def Movie_details():
    return render_template('Movie_details.html')

@app.route('/Movie_details2')
def Movie_details2():
    return render_template('Movie_details2.html')

@app.route('/Movie_details3')
def Movie_details3():
    return render_template('Movie_details3.html')

def create_user(name, username, email, password, credit_card_number):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='movie_theater_storage',
                                             user='root',
                                             password='turbo')
        cursor = connection.cursor()

        # Check if the credit card number is valid
        if not is_valid_credit_card(credit_card_number):
            return False

        # Insert the new user into the database
        query = "INSERT INTO users (name, username, email, password, credit_card_number) VALUES (%s, %s, %s, %s, %s)"
        values = (name, username, email, password, credit_card_number)
        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

        return True

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
        credit_card_number = request.form['credit_card_number']

        # Check if the username is already taken
        if get_user_id(username):
            return render_template('Register_account.html') + render_template('Register_Error_Popup.html')

        # If the username is not taken and the credit card number is valid, create a new user in the database
        if create_user(name, username, email, password, credit_card_number):
            return render_template('Landing_Page.html') + render_template('Register_successful_popup.html')
        else:
            return render_template('Register_account.html') + render_template('Invalid_credit_card_popup.html')



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


@app.route('/book_movie1', methods=['POST'])
def book_movie1():
    # Highlight 3 Get the movie_id from the form data USE THIS TO CHANGE WHAT MOVIE IS BOOKED
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
        error_message = "Failed to insert record into bookings table: {}".format(error)
        return render_template('popup_book_failed.html') + render_template('Landing_Page.html')

    return render_template('Landing_Page.html') + render_template('popup_book_done.html')


@app.route('/book_movie2', methods=['POST'])
def book_movie2():
    movie_id = '2'

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

    return render_template('Landing_Page.html')

@app.route('/book_movie3', methods=['POST'])
def book_movie3():
    movie_id = '3'

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

    return render_template('Landing_Page.html')

@app.route('/Logout')
def Logout():
    session.pop('user_id', None)
    return render_template('Landing_Page.html') +render_template('Logout_Popup.html')

@app.route('/Payment')
def Payment():
    return render_template('Payment.html')

def is_valid_credit_card(number):
    # Check if the length is correct
    if len(number) != 16:
        return False
    #Highlight 2
    # Luhn algorithm
    total = 0
    for i, digit in enumerate(number):
        # Multiply every other digit by 2, starting from the second-to-last digit
        if i % 2 == 0:
            doubled_digit = int(digit) * 2
            if doubled_digit > 9:
                # If the result is greater than 9, subtract 9 from it
                doubled_digit -= 9
            total += doubled_digit
        else:
            total += int(digit)
    
    # The credit card number is valid if the sum of all digits is a multiple of 10
    return total % 10 == 0

if __name__ == '__main__':
    app.run(debug=True)
