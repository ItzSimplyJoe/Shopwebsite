from databasecommands import *
'''
to insert a new record
insert_item("itemname","quantity","price")
Then simply run this file

or to insert a new user
insert_user("email","password")
Then simply run this file

or to insert a new order
insert_order("user_id","item_id","quantity")
Then simply run this file
'''
create_table_item()
create_table_user()
create_table_orders()