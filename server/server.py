import socket
import threading
import json
import os
import time
import re
from client.client import COMMAND_PAYMENT
from db import Database
from datetime import datetime

# MESSAGE
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# COMMAND
COMMAND_INFO = "!INFO"
COMMAND_ORDER = "!ORDER"
COMMAND_PAYMENT = "!PAYMENT"

# # CARD REGEX
# CARD_REGEX = "^\d{10}$"

class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname()) or '127.0.0.1'
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

    def send_total_price(self, conn, addr, total_price):
        conn.send(b'!TOTAL_PRICE')
        time.sleep(0.01)
        conn.send(str(total_price).encode(FORMAT))

    def send_order_id(self, conn, addr, order_id):
        conn.send(b'!ORDER_ID')
        time.sleep(0.01)
        conn.send(str(order_id).encode(FORMAT))

    def handle_menu_request(self, conn, addr):
        time.sleep(1)
        #Get menu list from database then send to client
        menu = self.database.get_menu()
        conn.send(b'!MENU_LIST')
        time.sleep(0.001)
        conn.send(json.dumps(menu).encode())
        time.sleep(0.001)
        conn.send(b'!END_MENU_LIST')
        time.sleep(0.001)

        # Iterate image and send image to client
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
        conn.send(b'!MENU_DONE')
                
    def handle_order_request(self, conn, addr, request):
        order_data = request['data']
        print(f"[ORDER_DETAIL] {addr} ordered {order_data}")

        # Get the neccesary order information and insert to database
        order_user_id = order_data['user_id']
        order_date = order_data['date']
        order_detail = order_data['order']
        self.database.insert_order(order_user_id, order_date, order_detail)

        # Calculate total price
        order_id = int(self.database.get_order_id(order_user_id, order_date))
        print(f"[ORDER_ID] {order_id}")
        print(type(order_id))
        order_total_price = self.database.get_total_price(order_id)
        print(f"[ORDER] total calculated: {order_total_price}")

        time.sleep(0.01)
        self.send_total_price(conn, addr, order_total_price)
        time.sleep(0.01)
        self.send_order_id(conn, addr, order_id)
        time.sleep(0.01)
        conn.send(b'!ORDER_DONE')

    def handle_payment_request(self, conn, addr, request):
        payment_option = request['data']["option"]
        order_id = request['data']["order_id"]

        if (payment_option == 'cash'):
            print(f"[PAYMENT] {addr} paid by cash")
            self.database.update_order_paid_status(order_id, True)
    
        elif (payment_option == 'card'):
            card_details = str(request['data']["card_details"])
            if (card_details.isnumeric() and len(card_details) == 10 and card_details[0] != '0'):
                print(f"[PAYMENT] {addr} paid by card")
                self.database.update_order_paid_status(order_id, True)
            else:
                conn.send(b'!PAYMENT_FAIL')

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

                # Handle client request
                if (msg["header"] == COMMAND_INFO):
                    print(f"[INFO] {addr} requested menu")
                    self.handle_menu_request(conn, addr)

                elif (msg["header"] == COMMAND_ORDER):
                    print(f"[ORDER] {addr} made an order")
                    self.handle_order_request(conn, addr, msg)

                elif (msg["header"] == COMMAND_PAYMENT):
                    print(f"[PAYMENT] {addr} paid")
                    self.handle_payment_request(conn, addr, msg)
                    
            except socket.error:
                print(f"[ERROR] {addr} disconnected")
                connected = False
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
        
    
