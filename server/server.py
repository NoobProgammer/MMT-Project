import socket
import threading
import json
import os
import time
from db import Database
from datetime import datetime

# MESSAGE
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# COMMAND
COMMAND_INFO = "!INFO"
COMMAND_ORDER = "!ORDER"

from struct import pack

class Server:
    def __init__(self):
        self.ip = '127.0.0.2'
        self.port = 12345
        self.addr = (self.ip, self.port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
        self.database = Database('restaurant.db')

    def start(self):
        self.server.listen(5)
        print(f'[LISTENING] Listening on {self.ip} on port {self.port}')

        while True:
            conn, addr = self.server.accept()
            # Create a new thread for each connection to handle the client
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle_menu_request(self, conn, addr):
        #Get menu list from database then send to client
        menu = self.database.get_menu()
        conn.send(b'!MENU_LIST')
        time.sleep(0.001)
        conn.send(json.dumps(menu).encode())
        time.sleep(0.001)
        conn.send(b'!END_MENU_LIST')
        time.sleep(0.001)

        # Iterate image and send to client
        for file in os.scandir(path='./img'):
            if file.is_file():
                conn.send(b'!MENU_IMG')
                time.sleep(0.01)
                f = open(file.path, 'rb')
                bytes = f.read(1024)
                while bytes:
                    conn.send(bytes)
                    bytes = f.read(1024)
                
                f.close()
                time.sleep(0.05)
                conn.send(b'!END_IMG')
            time.sleep(0.05)
        # Done everything, send end message
        time.sleep(0.01)
        conn.send(b'!DONE')
                
    def handle_order_request(self, request, addr):
        print(f"[ORDER] {addr} made an order")
        print(request)
        print('----------------------------------------------------')
        orderData = request['data']
        print(orderData)
        user_id = orderData['user_id']
        date = orderData['date']
        order = orderData['order']
        self.database.insert_order(user_id, date, order)
        total = self.database.conn.execute("SELECT total FROM orders WHERE user_id = ? AND date = ?", (user_id, date)).fetchone()[0]
        time.sleep(0.01)
        
        return total
        
       
    # Handle connection with client
    # conn is the connection
    # addr is the address of the client
    # Handle jobs according to client request
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")
        connected = True
        while connected:
            try:
                msg = json.loads(conn.recv(1024).decode(FORMAT))
                if (msg["header"] == COMMAND_INFO):
                    print(f"[INFO] {addr} requested menu")
                    self.handle_menu_request(conn, addr)
                    #self.handle_menu_img_request(conn, addr)
                if (msg["header"] == COMMAND_ORDER):
                    total_calculated = self.handle_order_request(msg, addr)
                    conn.send(str(total_calculated).encode(FORMAT))
                    print(f"[ORDER] total calculated: {total_calculated}")
                    time.sleep(0.01)
                    

            # except socket.error:
            #     print(f"[ERROR] {addr} disconnected")
            #     connected = False
            except json.JSONDecodeError:
                print(f"[DISCONNECTED] {addr} disconnected")
                connected = False

        conn.close()


if __name__ == '__main__':
    server = Server()
    print("[STARTING] server is starting")
    try:
        server.start()
    except KeyboardInterrupt:
        exit()
        
    
