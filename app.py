from flask import Flask, render_template, request, session, redirect, url_for
from databasecommands import *
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_failed = False
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in'] == True:
            return redirect(url_for('Accountpage'))
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password = encryptpassword(password)
        value, id = userlogin(email, password)
        if value == True:
            session['logged_in'] = True
            session['user_id'] = id
            return redirect(url_for('Accountpage'))
        else:
            login_failed = True
            return render_template('login.html', login_failed=login_failed)

@app.route('/signup', methods=['GET','POST'])
def signup():
    inuse = False
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in'] == True:
            return redirect(url_for('Accountpage'))
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        value = checkuser(email)
        if value == True:
            inuse = True
        else:
            password = encryptpassword(password)
            insert_user(email, password)
            return render_template('login.html')
    return render_template('signup.html', inuse=inuse)

@app.route('/Accountpage')
def Accountpage():
    if 'logged_in' in session and session['logged_in'] == True:
        password_changed = request.args.get('password_changed') == 'True'
        id = session.get('user_id')
        user_orders = []
        user_data = checkuserbasedonid(id)
        email = user_data[0][1]
        password = user_data[0][2]
        user_orders = getuserorders(id)
        return render_template('Accountpage.html', user_orders=user_orders,email=email,password=password,password_changed=password_changed)

    else:
        return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add-to-cart/<item>')
def add_to_cart(item):
    if 'cart' not in session:
        session['cart'] = {}
    session['cart'][item] = session['cart'].get(item, 0) + 1
    return 'Item added to cart!'

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    password_changed = False
    id = session.get('user_id')
    user_data = checkuserbasedonid(id)
    email = user_data[0][1]
    password = user_data[0][2]
    if request.method == 'POST':
        newpassword = request.form['password']
        if len(newpassword) < 3:
            return render_template('Accountpage.html', email=email, password=password, password_changed=password_changed)
        else:
            newpassword = encryptpassword(newpassword)
            updatepassword(email, newpassword)
            password_changed = True
            return redirect(url_for('Accountpage', password_changed=password_changed))
    return render_template('Accountpage.html', email=email, password=password, password_changed=password_changed)

@app.route('/changepassword', methods=['POST'])
def change_password():
    id = session.get('user_id')
    user_data = checkuserbasedonid(id)
    email = user_data[0][1]
    newpassword = request.form['password']
    user_orders = getuserorders(id)
    if newpassword > 8:
        user = True
    else:
        user = False
    if user:
        newpassword = encryptpassword(newpassword)
        updatepassword(email, newpassword)
        return redirect('/Accountpage?password_changed=True')
    else:
        return redirect('/Accountpage?password_changed=False')
    

if __name__ == '__main__':
    app.run(debug=True)