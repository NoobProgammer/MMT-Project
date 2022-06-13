import sqlite3
import base64

# Comment out for later use
# Will implement a database instead of json files


create_users_table_sql = """ CREATE TABLE IF NOT EXISTS users (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [username] TEXT NOT NULL,
    [balance] INTEGER NOT NULL DEFAULT 0
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
    [user_id] INTEGER NOT NULL,
    [menu_id] INTEGER NOT NULL,
    [quantity] INTEGER NOT NULL,
    [total] INTEGER NOT NULL,
    [date] TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(menu_id) REFERENCES menu(id)
)"""

create_table_queries = [create_users_table_sql,
           create_menu_table_sql, create_orders_table_sql]


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

    #Create section
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

    def insert_order(self, order):
        pass

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

    #Update section
    def update_order(self):
        pass

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
    db = Database('restaurant.db')
    # Run code below only once to initiate database

    db.create_table(create_table_queries[0])
    db.create_table(create_table_queries[1])
    db.create_table(create_table_queries[2])

    db.insert_food({
        'name': 'Pizza',
        'price': 100,
        'description': 'This is a pizza',
        'image': './1.jpg'
    })
    # db.insert_food({
    #     'name': 'Pasta',
    #     'price': 200,
    #     'description': 'This is a pasta',
    #     'image': 'some image'
    # })
    # db.insert_food({
    #     'name': 'Salad',
    #     'price': 300,
    #     'description': 'This is a salad',
    #     'image': 'some image'
    # })
    # db.insert_food({
    #     'name': 'Rice',
    #     'price': 400,
    #     'description': 'This is rice',
    #     'image': 'some image'
    # })
    # menu = db.get_menu()

    # with open('./string.txt', 'w') as file:
    #     file.write(menu[0]['image'].decode('utf-8'))
