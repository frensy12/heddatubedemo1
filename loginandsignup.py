from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
import os

app = Flask(__name__, static_folder='static')
app.secret_key = 'ostepotetmedsauspå8932'  # Set a secret key for session management

# Helper functions
def read_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            users.append({'username': username, 'password': password})
    return users

def write_user(username, password):
    with open('users.txt', 'a') as file:
        file.write(f'{username},{password}\n')

# Routes
@app.route('/')
def home():
    return send_from_directory('static', 'loginandsignup.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    users = read_users()

    # Check if username already exists
    if any(user['username'] == username for user in users):
        return 'Brukernavnet er tatt.'

    # Add the new user
    write_user(username, password)

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    users = read_users()

    # Check if the username and password match
    if any(user['username'] == username and user['password'] == password for user in users):
        # Set a session cookie to remember the user
        response = make_response(redirect(url_for('index')))
        response.set_cookie('username', username)
        return response
    else:
        return 'Feil Brukernavn eller passord'

@app.route('/index')
def index():
    # Retrieve username from the session cookie
    username = request.cookies.get('username', None)
    return render_template('index.html', username=username)

@app.route('/upload')
def upload():
    # Retrieve username from the session cookie
    username = request.cookies.get('username', None)
    return render_template('upload.html', username=username)

if __name__ == '__main__':
    # Initialize users.txt if it doesn't exist
    if not os.path.exists('users.txt'):
        open('users.txt', 'a').close()

    app.run(debug=True)
