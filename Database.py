import sqlite3

# connect to the database
with sqlite3.connect('dream_waters_inventory.db', timeout=5) as conn:

# create a cursor
    c = conn.cursor()

# create a table for products
#c.execute('''CREATE TABLE products
             #(product_id INTEGER PRIMARY KEY AUTOINCREMENT,
              #product_name TEXT NOT NULL,
              #quantity INTEGER NOT NULL,
              #unit_price REAL NOT NULL,
              #date_added DATE NOT NULL)''')

# create a table for sales
#c.execute('''CREATE TABLE sales
             #(sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
              #product_id INTEGER NOT NULL,
              #quantity INTEGER NOT NULL,
              #total_price REAL NOT NULL,
              #date_sold DATE NOT NULL,
              #FOREIGN KEY(product_id) REFERENCES products(product_id))''')

# create a table for user accounts
#c.execute('''CREATE TABLE accounts
             #(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
              #username TEXT UNIQUE NOT NULL,
              #password TEXT NOT NULL,
              #is_admin INTEGER NOT NULL)''')
              
#c.execute('''ALTER TABLE accounts ADD COLUMN security_question TEXT NULL''')

#c.execute('''ALTER TABLE accounts ADD COLUMN security_answer TEXT''')

#c.execute('''ALTER TABLE accounts ADD COLUMN email TEXT''')

#c.execute(''' ALTER TABLE accounts ADD COLUMN role TEXT NOT NULL DEFAULT "user"''')
#c.execute('''ALTER TABLE products ADD COLUMN category TEXT''')


    # Create a table for history
    #c.execute('''CREATE TABLE history
                 #(action_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  #action_type TEXT NOT NULL,
                  #product_id INTEGER NOT NULL,
                  #user_id INTEGER NOT NULL,
                  #action_date DATETIME NOT NULL,
                  #FOREIGN KEY(product_id) REFERENCES products(product_id),
                  #FOREIGN KEY(user_id) REFERENCES accounts(user_id))''')
    #c.execute("ALTER TABLE history ADD COLUMN Category TEXT")
   # c.execute("ALTER TABLE history ADD COLUMN Product_Name TEXT")


# commit the changes and close the connection
    #conn.commit()
    #conn.close
    #c.execute("ALTER TABLE history ALTER COLUMN product_id DROP NOT NULL")
    #c.execute("ALTER TABLE history ALTER COLUMN user_id DROP NOT NULL")
    
    #c.execute("ALTER TABLE history ADD COLUMN user TEXT")
    
    c.execute("ALTER TABLE history RENAME TO history_old")  # Rename the existing table
    c.execute('''CREATE TABLE history
                (action_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT NOT NULL,
                product_id INTEGER,
                product_name TEXT,
                category TEXT,
                user TEXT,
                action_date DATETIME NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(product_id))''')
    c.execute("INSERT INTO history (action_type, product_id, product_name, category, action_date) SELECT action_type, product_id, product_name, category, action_date FROM history_old")
    c.execute("DROP TABLE history_old")  # Drop the old table
    conn.commit()


