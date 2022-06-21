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
<<<<<<< Updated upstream

from struct import pack
=======
COMMAND_PAYMENT = "!PAYMENT"
COMMAND_EXTEND = "!EXTEND"
COMMAND_EXTRA = "!EXTRA"
# # CARD REGEX
# CARD_REGEX = "^\d{10}$"
>>>>>>> Stashed changes

class Server:
    def __init__(self):
        self.ip = '127.0.0.1'
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
        time.sleep(3)
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
<<<<<<< Updated upstream
        
        return total
        
       
=======
        conn.send(json.dumps(client_order).encode(FORMAT))

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

    def handle_extend_request(self, conn, addr, request):
        order_id = request['data']['order_id']
        flag = self.database.check_done_status(order_id)
        if (flag == 1):
            conn.send(b'!EXTEND_TRUE')
        elif(flag == 0):
            conn.send(b'!EXTEND_FALSE')
            
    def handle_extra_request(self, conn, addr, request):
        order_data = request['data']
        print(f"[ORDER_DETAIL] {addr} ordered extra {order_data}")
        
        # Get the neccesary order information and insert to database
        order_id = order_data['order_id']
        order_detail = order_data['order']
        self.database.insert_order(order_id, order_detail)
        
        # Calculate total price
        order_total_price = self.database.get_total_price(order_id)
        print(f"[ORDER_ID] {order_id}")
        print(f"[ORDER] total calculated: {order_total_price}")
        client_order = {
            "id": order_id,
            "total_price": order_total_price
        }

        conn.send(b'!ORDER_PRICE')
        time.sleep(0.01)
        conn.send(json.dumps(client_order).encode(FORMAT))
            
    
>>>>>>> Stashed changes
    # Handle connection with client
    # conn is the connection
    # addr is the address of the client
    # Handle jobs according to client request
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")
        connected = True
        while connected:
            # Need to tweak this more before calling because newly created database doesnt have any rows which will cause bugs
            # self.database.update_done_database()
            # self.database.update_total_database()
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
                    
<<<<<<< Updated upstream

            # except socket.error:
            #     print(f"[ERROR] {addr} disconnected")
            #     connected = False
=======
                elif (msg["header"] == COMMAND_EXTEND):
                    print(f'[EXTEND] {addr} wants to extend')
                    self.handle_extend_request(conn, addr, msg)
                    
                elif (msg["header"] == COMMAND_EXTRA):
                    print(f'[EXTRA] {addr} ordered extra')
                    self.handle_extra_request(conn, addr, msg)
                    
            except socket.error:
                print(f"[ERROR] {addr} disconnected")
                connected = False
>>>>>>> Stashed changes
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
        
    
