from flask import Flask, render_template, request
from databasecommands import *

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    insert_user(email, password)

    return 'Login successful'

@app.route('/')
def index():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
