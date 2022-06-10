from multiprocessing import Event
import socket
import threading
import json
import time

# MESSAGE
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# COMMAND
COMMAND_INFO = "!INFO"
COMMAND_ORDER = "!ORDER"


class Server:
    def __init__(self):
        self.ip = '127.0.1.1'
        self.port = 12345
        self.addr = (self.ip, self.port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)

    def start(self):
        self.server.listen(5)
        print(f'[LISTENING] Listening on {self.ip} on port {self.port}')

        while True:
            conn, addr = self.server.accept()
            # Create a new thread for each connection to handle the client
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def receive_menu_request(self, conn, addr):
        menu = json.load(open("menu.json"))
        # Send back the menu to client
        conn.send(json.dumps(menu).encode(FORMAT))

    def receive_order_request(self, request, addr):
        menu_id = request['data']
        f = open("menu.json")
        menu = json.load(f)

        # Create a new order (temporary, will implement database later)
        order = {
            'id': menu_id,
            'quantity': 2,
            'table_number': 3,
            'date': '',
            'status': ''
        }

        for item in menu:
            if item['id'] == menu_id:
                order['menu_id'] = item['id']
                order['menu_name'] = item['name']
                order['price'] = item['price'] * order['quantity']
                break
        
        # Save order to file
        orders = json.load(open("orders.json"))
        orders.append(order)
        with open("orders.json", "w") as f:
            json.dump(orders, f)
        
            
    # Handle connection with client
    # conn is the connection
    # addr is the address of the client
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")

        connected = True
        while connected:
            try:
                msg = json.loads(conn.recv(1024).decode(FORMAT))
                if (msg["header"] == COMMAND_INFO):
                    print(f"[INFO] {addr} requested menu")
                    self.receive_menu_request(conn, addr)
                if (msg["header"] == COMMAND_ORDER):
                    self.receive_order_request(msg, addr)
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
