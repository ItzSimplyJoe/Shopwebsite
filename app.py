from flask import Flask, render_template, request, session, redirect, url_for
from databasecommands import *
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
def getuserbasket():
    if 'logged_in' in session and session['logged_in'] == True:
        id = session.get('user_id')
        basket = getbasketitems(id)
        cart_count = len(basket)
        return basket, cart_count
    else:
        if 'cart' in session:
            cart = session['cart']
            cart_count = len(cart)
            return cart, cart_count
        else:
            cart_count = 0
            return [], cart_count
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    basket,cart_count = getuserbasket()
    login_failed = False
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in'] == True:
            return redirect(url_for('Accountpage'))
        return render_template('login.html', cart_count=cart_count)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password = encryptpassword(password)
        value, id = userlogin(email, password)
        if value == True:
            session['logged_in'] = True
            session['user_id'] = id
            basket, cart_count = getuserbasket()
            return redirect(url_for('Accountpage'))
        else:
            login_failed = True
            return render_template('login.html', login_failed=login_failed, cart_count=cart_count)

@app.route('/signup', methods=['GET','POST'])
def signup():
    inuse = False
    basket,cart_count = getuserbasket()
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
            return render_template('login.html', cart_count=cart_count)
    return render_template('signup.html', inuse=inuse, cart_count=cart_count)

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
        basket,cart_count = getuserbasket()
        return render_template('Accountpage.html', user_orders=user_orders,email=email,password=password,password_changed=password_changed, cart_count=cart_count)
    else:
        return redirect(url_for('login'))
@app.route('/cart')
def cart():
    basket, cart_count = getuserbasket()
    items = []
    for item in basket:
        iteminfo = getiteminfo(item)
        item_dict = {
            'name': iteminfo[0][1],
            'quantity': 1,
            'price': iteminfo[0][3],
            'image_url': f'/static/images/{iteminfo[0][0]}.png'
        }
        items.append(item_dict)
    return render_template('cart.html', items=items, cart_count=cart_count)

@app.route('/')
def index():
    basket,cart_count = getuserbasket()
    return render_template('index.html', cart_count=cart_count)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/product')
def product():
    basket,cart_count = getuserbasket()
    return render_template('product.html', cart_count = cart_count)

@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    password_changed = False
    id = session.get('user_id')
    user_data = checkuserbasedonid(id)
    email = user_data[0][1]
    password = user_data[0][2]
    basket,cart_count = getuserbasket()
    if request.method == 'POST':
        newpassword = request.form['password']
        if len(newpassword) < 3:
            return render_template('Accountpage.html', email=email, password=password, password_changed=password_changed, cart_count=cart_count)
        else:
            newpassword = encryptpassword(newpassword)
            updatepassword(email, newpassword)
            password_changed = True
            return redirect(url_for('Accountpage', password_changed=password_changed))
    return render_template('Accountpage.html', email=email, password=password, password_changed=password_changed, cart_count=cart_count)


@app.route('/about')
def about():
    basket,cart_count = getuserbasket()
    return render_template('about.html', cart_count=cart_count)

@app.route('/add-to-cart/<int:id>')
def addtocartfromabout(id):
    basket,cart_count = getuserbasket()
    if 'logged_in' in session and session['logged_in'] == True:
        userid = session.get('user_id')
        try:
            addtobasket(userid, id)
        except:
            return render_template('about.html', id=id, cart_count=cart_count)
    else:
        if 'cart' in session:
            cart = session['cart']
            cart.append(id)
            session['cart'] = cart
        else:
            cart = []
            cart.append(id)
            session['cart'] = cart
    return render_template('about.html', id=id, cart_count=cart_count+1)

@app.route('/removefromcart/<int:id>')
def removefromcart(id):
    basket,cart_count = getuserbasket()
    if 'logged_in' in session and session['logged_in'] == True:
        userid = session.get('user_id')
        removeitemfrombasket(userid, id)
    else:
        if 'cart' in session:
            cart = session['cart']
            cart.remove(id)
            session['cart'] = cart
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
