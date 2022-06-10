# import sqlite3

# Comment out for later use
# Will implement a database instead of json files


# create_users_table_sql = """ CREATE TABLE IF NOT EXISTS users (
#     [id] INTEGER PRIMARY KEY AUTOINCREMENT,
#     [username] TEXT NOT NULL,
#     [balance] INTEGER NOT NULL DEFAULT 0
# )"""

# create_menu_table_sql = """ CREATE TABLE IF NOT EXISTS menu (
#     [id] INTEGER PRIMARY KEY AUTOINCREMENT,
#     [name] TEXT NOT NULL,
#     [price] INTEGER NOT NULL,
#     [description] TEXT NOT NULL,
#     [image] TEXT NOT NULL
# )"""

# create_orders_table_sql = """ CREATE TABLE IF NOT EXISTS orders (
#     [id] INTEGER PRIMARY KEY AUTOINCREMENT,
#     [user_id] INTEGER NOT NULL,
#     [menu_id] INTEGER NOT NULL,
#     [quantity] INTEGER NOT NULL,
#     [total] INTEGER NOT NULL,
#     [date] TEXT NOT NULL,
#     FOREIGN KEY(user_id) REFERENCES users(id),
#     FOREIGN KEY(menu_id) REFERENCES menu(id)
# )"""

# queries = [create_users_table_sql,
#            create_menu_table_sql, create_orders_table_sql]


# class Database:
#     def __init__(self, db, create_table_queries):
#         self.conn = sqlite3.connect(db)
#         if (self.conn is not None):
#             try:
#                 self.cur = self.conn.cursor()
#                 for query in create_table_queries:
#                     self.cur.execute(query)
#             except OSError as e:
#                 print(e)
#         self.conn.commit()

#     def fetch(self):
#         pass

    

# if __name__ == '__main__':
#     db = Database('restaurant', queries)