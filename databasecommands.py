import sqlite3

def create_table_item():
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS store (
        itemid INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price FLOAT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_item(item, quantity, price):
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO store VALUES (?,?,?,?)", (None, item, quantity, price))
    conn.commit()
    conn.close()

def view_item():
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_item(item):
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM store WHERE item=?", (item,))
    conn.commit()
    conn.close()

def getitemid(item):
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM store WHERE item=?", (item,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]

def getiteminfo(itemid):
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM store WHERE itemid=?", (itemid,))
    rows = cur.fetchall()
    conn.close()
    return rows
############################################## User Database ##############################################
def create_table_user():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        basket TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_user(email, password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?,?)", (None,email, password, None))
    conn.commit()
    conn.close()

def view_user():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_user(email):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()

def userlogin(email, password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    rows = cur.fetchall()
    conn.close()
    if rows == []:
        return False,None
    else:
        return True, rows[0][0]
    
def checkuser(email):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    rows = cur.fetchall()
    conn.close()
    if rows == []:
        return False
    else:
        return True
    
def checkuserbasedonid(userid):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE userid=?", (userid,))
    rows = cur.fetchall()
    conn.close()
    return rows

def encryptpassword(password):
    password = password[::-1]
    return password

def updatepassword(email,password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=? WHERE email=?", (password,email))
    conn.commit()
    conn.close()
############################################## Basket Database ##############################################  
def addtobasket(email,itemid):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    rows = cur.fetchall()
    basket = rows[0][3]
    if basket == None:
        basket = str(itemid)
    else:
        basket = basket + "," + str(itemid)
    cur.execute("UPDATE users SET basket=? WHERE email=?", (basket,email))
    conn.commit()
    conn.close()

def clearbasket(email):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET basket=? WHERE email=?", (None,email))
    conn.commit()
    conn.close()

def removeitemfrombasket(email,itemid):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    rows = cur.fetchall()
    basket = rows[0][3]
    basket = basket.split(",")
    basket.remove(str(itemid))
    basket = ",".join(basket)
    cur.execute("UPDATE users SET basket=? WHERE email=?", (basket,email))
    conn.commit()
    conn.close()

def getbasketitems(email):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    rows = cur.fetchall()
    basket = rows[0][3]
    basket = basket.split(",")
    conn.close()
    return basket

def getbaskettotal(email):
    basket = getbasketitems(email)
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    total = 0
    for item in basket:
        cur.execute("SELECT * FROM store WHERE itemid=?", (item,))
        rows = cur.fetchall()
        total += rows[0][2]
    conn.close()
    return total

def getitemdetails(itemid):
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM store WHERE itemid=?", (itemid,))
    rows = cur.fetchall()
    conn.close()
    return rows[1]

############################################## orders Database ##############################################  
def create_table_orders():
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        orderid INTEGER PRIMARY KEY AUTOINCREMENT,
        userid INTEGER NOT NULL,
        itemid INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price FLOAT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_order(userid, itemid, quantity, price):
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO orders VALUES (?,?,?,?,?)", (None, userid, itemid, quantity, price))
    conn.commit()
    conn.close()

def view_orders():
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_order(orderid):
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE orderid=?", (orderid,))
    conn.commit()
    conn.close()

def getuserorders(userid):
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE userid=?", (userid,))
    rows = cur.fetchall()
    conn.close()
    return rows

