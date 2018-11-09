import sqlite3
from sqlite3 import Error


conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS links''')
c.execute('''DROP TABLE IF EXISTS products_specs''')
c.execute('''DROP TABLE IF EXISTS products_forms''')

# Create table
c.execute('''CREATE TABLE links (ID INTEGER PRIMARY KEY AUTOINCREMENT, url text NOT NULL UNIQUE, downloaded INTEGER, same_domain INTEGER, tmst TEXT)''')
c.execute('''CREATE TABLE products_specs (ID INTEGER PRIMARY KEY AUTOINCREMENT, ID_url, attribute_name, attribute_value)''')
c.execute('''CREATE TABLE products_forms (ID INTEGER PRIMARY KEY AUTOINCREMENT, ID_url, ID_prod, form_id, form_field_id, form_field_value)''')
conn.commit

conn.close()
c.close()



