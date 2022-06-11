import socket
import json
import threading
import time

# MESSAGE
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# COMMAND
COMMAND_INFO = "!INFO"
COMMAND_ORDER = "!ORDER"

class Client:
    def __init__(self):
        # Connection info
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.target_server_ip = ''
        self.port = 0
        self.addr = ()

    def connect(self):
        self.target_server_ip = input("Enter the server IP: ")
        self.port = int(input("Enter the server port: "))
        self.addr = (self.target_server_ip, self.port)
        timeout = None

        disconnected = True
        print("[CONNECTING] Connecting to server...")
        while disconnected:
            try:
                self.client.connect(self.addr)
                # self.client.settimeout(None)
                disconnected = False
                print("[SUCCESS] Connected to server")
            except TimeoutError:
                print("[ERROR] Connection timeout")
                exit()
            except ConnectionRefusedError:
                pass
            except ConnectionAbortedError:
                pass
            

    def encapsulate_request(self, header, data):
        return json.dumps({"header": header, "data": data}).encode(FORMAT)

    def request_menu(self):
        request = self.encapsulate_request(COMMAND_INFO, "")
        self.client.send(request)

    def make_order(self, id):
        request = self.encapsulate_request(COMMAND_ORDER, id)
        self.client.send(request)

    def on_receive_menu(self):
        while True:
            print("[WAITING] Waiting for response")
            try:
                menu = json.loads(self.client.recv(1024).decode(FORMAT))
                print("[SUCCESS] Received menu")
                return menu
            except OSError: 
                break

    def format_menu(self, menu):
        message = ""
        for item in menu:
            message += f"{item['name']} - {item['price']} VND\n"
        return message

    