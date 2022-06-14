import socket
import json
import threading
import time
from struct import unpack

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

    def make_order(self, order):
        request = self.encapsulate_request(COMMAND_ORDER, order)
        self.client.send(request)

    def on_receive_menu(self):
        index = 1
        print('[WAITING] Waiting for menu response')
        while True:
            msg = self.client.recv(1024)
            # Check msg type
            if (msg == b'!MENU_LIST'):
                # Receive menu list
                while True:
                    msg = self.client.recv(1024)
                    if (msg != b'!END_MENU_LIST'):
                        print('[RECEIVED] Menu received')
                        menu = json.loads(msg.decode(FORMAT))
                    else:
                        break       
            elif (msg == b'!MENU_IMG'):
                with open(f"./img/{index}.jpg", "wb") as f:
                    while True:
                        msg = self.client.recv(1024)
                        if (msg == b'!END_IMG'):
                            index += 1
                            break
                        else:
                            f.write(msg)
            elif(msg == b'!DONE'):
                print('[DONE] Receiving process done')
                return menu
 
    def format_menu(self, menu):
        message = ""
        for item in menu:
            message += f"{item['name']} - {item['price']} VND\n"
        return message

    