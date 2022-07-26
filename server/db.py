import sqlite3
import base64
from datetime import datetime

# Comment out for later use
# Will implement a database instead of json files

create_users_table_sql = """ CREATE TABLE IF NOT EXISTS users (
    [id] TEXT PRIMARY KEY
)"""

create_menu_table_sql = """ CREATE TABLE IF NOT EXISTS menu (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [price] INTEGER NOT NULL,
    [description] TEXT NOT NULL,
    [image] TEXT NOT NULL
)"""

create_orders_table_sql = """ CREATE TABLE IF NOT EXISTS orders (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [user_id] TEXT NOT NULL,
    [total] INTEGER NOT NULL,
    [date] TEXT NOT NULL,
    [done] BOOLEAN NOT NULL default 0,
    [paid] BOOLEAN NOT NULL default 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
)"""


create_orders_detail_table_sql = """ CREATE TABLE IF NOT EXISTS orders_detail (
    [order_id] INTEGER NOT NULL,
    [menu_id] INTEGER NOT NULL,
    [quantity] INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(menu_id) REFERENCES menu(id)
    
)"""

create_table_queries = [create_users_table_sql,
                        create_menu_table_sql, create_orders_table_sql, create_orders_detail_table_sql]
class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        if (self.conn is not None):
            try:
                self.cur = self.conn.cursor()
            except OSError as e:
                print(e)
        self.conn.commit()

    def fetch(self):
        pass

    # Create section
    def create_table(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def insert_food(self, food):
        # Convert image to string
        # with open(img_path, "rb") as file:
        #     converted_string = base64.b64encode(file.read())

        self.conn.execute(
            "INSERT INTO menu (name, price, description, image) VALUES (?, ?, ?, ?)",
            (food['name'], food['price'], food['description'], food['image'])
        )
        self.conn.commit()

    def insert_order(self, user_id, date, order):
        self.conn.execute(
            f"INSERT INTO orders (user_id, date, total) VALUES ('{user_id}', '{date}', 999999999999)")
        order_id = self.conn.execute(
            f"SELECT id FROM orders WHERE user_id = '{user_id}' AND date = '{date}'").fetchone()[0]
        for food in order:
            self.conn.execute(
                f"INSERT INTO orders_detail (order_id, menu_id, quantity) VALUES ('{order_id}', '{food['id']}', '{food['quantity']}')")
        total = self.conn.execute(
            f"SELECT SUM(menu.price * orders_detail.quantity) FROM orders_detail INNER JOIN menu ON orders_detail.menu_id = menu.id WHERE orders_detail.order_id = '{order_id}'").fetchone()[0]
        self.conn.execute(
            f"UPDATE orders SET total = '{total}' WHERE id = '{order_id}'")
        self.conn.commit()
    
    def insert_extra_order(self,  order_id, order):
        for food in order:
            self.conn.execute(f"INSERT INTO orders_detail (order_id, menu_id, quantity) VALUES ('{order_id}', '{food['id']}', '{food['quantity']}')")
            self.conn.commit()

    # Read section
    def get_menu(self):
        arr = []
        # Return array of dictionaries of all food
        for row in self.conn.execute("SELECT * FROM menu"):
            arr.append({
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'description': row[3],
                'image': row[4]
            })
        return arr

    def get_order_id(self, order_user_id, order_date):
        return self.conn.execute("SELECT id FROM orders WHERE user_id = ? AND date = ?", (order_user_id, order_date)).fetchone()[0]

    def get_total_price(self, order_id):
        return self.conn.execute(f"SELECT total FROM orders WHERE id = '{order_id}'").fetchone()[0]
    
    def check_done_status(self, order_id):
        return self.conn.execute(f"SELECT done FROM orders WHERE id = '{order_id}'").fetchone()[0]
    
    def check_paid_status(self, order_id):
        return self.conn.execute(f"SELECT paid FROM orders WHERE id = '{order_id}'").fetchone()[0]
        

    # Update section
    # These functions to updates every order in the database

    # Update total in database
    def update_total(self, order_id):
        total = self.conn.execute(
            f"SELECT SUM(menu.price * orders_detail.quantity) FROM orders_detail INNER JOIN menu ON orders_detail.menu_id = menu.id WHERE orders_detail.order_id = '{order_id}'").fetchone()[0]
        self.conn.execute(
            f"UPDATE orders SET total = '{total}' WHERE id = '{order_id}'")
        self.conn.commit()
    def update_total_database(self):
        print('UPDATING TOTAL DB')
        order_id_array = self.conn.execute('SELECT id FROM orders').fetchall()
        for order_id in order_id_array:
            self.update_total(order_id[0])
        self.conn.commit()
    
    # Update done in database
    def update_done(self, order_id):
        date = self.conn.execute(
            f"SELECT date FROM orders WHERE id = '{order_id}'").fetchone()[0]
        date = str(date)
        date = datetime.strptime(date, "%m/%d/%Y, %H:%M:%S")
        now = datetime.now()
        delta = now - date
        if (delta.seconds > 7200):
            self.conn.execute(
                f"UPDATE orders SET done = 1 WHERE id = '{order_id}'")
            self.conn.commit()
        elif (delta.seconds <= 7200):
            self.conn.execute(
                f"UPDATE orders SET done = 0 WHERE id = '{order_id}'")
            self.conn.commit()
        
    def update_done_database(self):
        print('UPDATING DONE DB')
        order_id_array = self.conn.execute('SELECT id FROM orders').fetchall()
        for order_id in order_id_array:
            self.update_done(order_id[0])
        self.conn.commit()
        
        
    def update_order_paid_status(self, order_id, is_paid):
        if (is_paid):
            self.conn.execute(
                f"UPDATE orders SET paid = 1 WHERE id = '{order_id}'")
            
    # Delete section
    def delete_food(self, food_id):
        self.conn.execute(
            "DELETE FROM menu WHERE id = ?", (food_id)
        )
        self.conn.commit()

    def delete_menu(self):
        self.conn.execute(
            "DELETE FROM menu"
        )
        self.conn.commit()


if __name__ == '__main__':
    db = Database('./restaurant.db')
    # Run code below only once to initiate database

    # Create Tables
    for query in create_table_queries:
        db.create_table(query)

    db.insert_food({
        'name': 'Pizza',
        'price': 100,
        'description': 'This is a pizza',
        'image': 'img/1.jpg'
    })
    db.insert_food({
        'name': 'Pasta',
        'price': 200,
        'description': 'This is a pasta',
        'image': 'img/2.jpg'
    })
    db.insert_food({
        'name': 'Salad',
        'price': 300,
        'description': 'This is a salad',
        'image': 'img/3.jpg'
    })
    db.insert_food({
        'name': 'Rice',
        'price': 400,
        'description': 'This is rice',
        'image': 'img/4.jpg'
    })
    db.insert_food({
        'name': 'Chicken',
        'price': 500,
        'description': 'This is Chicken',
        'image': 'img/5.jpg'
    })

    # Imagine we have only six tables
    table_id = ['TABLE001', 'TABLE002', 'TABLE003',
                'TABLE004', 'TABLE005', 'TABLE006']
    for id in table_id:
        db.conn.execute(f"INSERT INTO users (id) VALUES ('{id}')")

    # menu = db.get_menu()

    # with open('./string.txt', 'w') as file:
    #     file.write(menu[0]['image'].decode('utf-8'))
