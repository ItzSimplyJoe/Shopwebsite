import sqlite3
import hashlib

def create_table_item():
    connection =sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS store (
        itemid INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price FLOAT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

def insert_item(item, quantity, price):
    connection =sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO store VALUES (?,?,?,?)", (None, item, quantity, price))
    connection.commit()
    connection.close()

def view_item():
    connection =sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM store")
    rows = cursor.fetchall()
    connection.close()
    return rows

def delete_item(item):
    connection =sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM store WHERE item=?", (item,))
    connection.commit()
    connection.close()

def getitemid(item):
    connection =sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM store WHERE item=?", (item,))
    rows = cursor.fetchall()
    connection.close()
    return rows[0][0]

def getiteminfo(itemid):
    connection =sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM store WHERE itemid=?", (itemid,))
    rows = cursor.fetchall()
    connection.close()
    return rows
############################################## User Database ##############################################
def create_table_user():
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        basket TEXT
    )
    ''')
    connection.commit()
    connection.close()

def insert_user(email, password):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (?,?,?,?)", (None,email, password, None))
    connection.commit()
    connection.close()

def view_user():
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    connection.close()
    return rows

def delete_user(email):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE email=?", (email,))
    connection.commit()
    connection.close()

def userlogin(email, password):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    rows = cursor.fetchall()
    connection.close()
    if rows == []:
        return False,None
    else:
        return True, rows[0][0]
    
def checkuser(email):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    rows = cursor.fetchall()
    connection.close()
    if rows == []:
        return False
    else:
        return True
    
def checkuserbasedonid(userid):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE userid=?", (userid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def encryptpassword(password):
    password = hashlib.sha256(password.encode()).hexdigest()
    return password

def updatepassword(email,password):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET password=? WHERE email=?", (password,email))
    connection.commit()
    connection.close()
############################################## Basket Database ##############################################  
def addtobasket(email,itemid):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    rows = cursor.fetchall()
    basket = rows[0][3]
    if basket == None:
        basket = str(itemid)
    else:
        basket = basket + "," + str(itemid)
    cursor.execute("UPDATE users SET basket=? WHERE email=?", (basket,email))
    connection.commit()
    connection.close()

def clearbasket(email):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET basket=? WHERE email=?", (None,email))
    connection.commit()
    connection.close()

def removeitemfrombasket(userid,itemid):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE userid=?", (userid,))
    rows = cursor.fetchall()
    basket = rows[0][3]
    try:
        basket = basket.split(",")
        basket.remove(str(itemid))
        basket = ",".join(basket)
    except:
        basket = None
    cursor.execute("UPDATE users SET basket=? WHERE userid=?", (basket,userid))
    connection.commit()
    connection.close()

def getbasketitems(userid):
    connection =sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE userid=?", (userid,))
    rows = cursor.fetchall()
    basket = rows[0][3]
    try:
        basket = basket.split(",")
    except:
        basket = []
    connection.close()
    return basket

def getbaskettotal(email):
    basket = getbasketitems(email)
    connection =sqlite3.connect("items.db")
    cursor = connection.cursor()
    total = 0
    for item in basket:
        cursor.execute("SELECT * FROM store WHERE itemid=?", (item,))
        rows = cursor.fetchall()
        total += rows[0][2]
    connection.close()
    return total

def getitemdetails(itemid):
    connection =sqlite3.connect("items.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM store WHERE itemid=?", (itemid,))
    rows = cursor.fetchall()
    connection.close()
    return rows[1]

############################################## orders Database ##############################################  
def create_table_orders():
    connection =sqlite3.connect("orders.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        orderid INTEGER PRIMARY KEY AUTOINCREMENT,
        userid INTEGER NOT NULL,
        itemid INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price FLOAT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

def insert_order(userid, itemid, quantity, price):
    connection =sqlite3.connect("orders.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO orders VALUES (?,?,?,?,?)", (None, userid, itemid, quantity, price))
    connection.commit()
    connection.close()

def view_orders():
    connection =sqlite3.connect("orders.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    connection.close()
    return rows

def delete_order(orderid):
    connection =sqlite3.connect("orders.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM orders WHERE orderid=?", (orderid,))
    connection.commit()
    connection.close()

def getuserorders(userid):
    connection =sqlite3.connect("orders.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders WHERE userid=?", (userid,))
    rows = cursor.fetchall()
    connection.close()
    return rows

