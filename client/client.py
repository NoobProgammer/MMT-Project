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

    def request_menu_img(self):
        pass

    def request_menu(self):
        request = self.encapsulate_request(COMMAND_INFO, "")
        self.client.send(request)

    def make_order(self, order):
        request = self.encapsulate_request(COMMAND_ORDER, order)
        self.client.send(request)

    def on_receive_menu_test(self):
        connected = True
        while connected:
            menu = json.loads(self.client.recv(1024).decode(FORMAT))
            if (menu):
                connected = False
                print(menu)
            
        return menu
        
    def on_receive_menu(self):
        index = 1
        menu = []
        while True:
            bs = self.client.recv(8)
            (length,) = unpack('>Q', bs)
            data = b''
            while len(data) < length:
                # doing it in batches is generally better than trying
                # to do it all in one go, so I believe.
                to_read = length - len(data)
                data += self.client.recv(
                    4096 if to_read > 4096 else to_read)
                with open(f"{index}.png", 'w') as fp:
                    fp.write(data)

                index += 1
        # while True:
        #     img_size = int(self.client.recv(2048).decode())
        #     amount = 0
        #     while amount < img_size:
        #         with open(f"{index}.png", "wb") as f:
        #             l = self.client.recv(2048)
        #             # if (data == b'!END'):
        #             #     f.close()
        #             #     index+=1
        #             # else:
        #             f.write(l)
        #             amount += len(l)
        #             index+=1

            


            # print("[WAITING] Waiting for response")
            # with open (f"./img/{index}.png", "wb") as f:
            #     try:
            #         while (True):
            #             data = self.client.recv(2048)
            #             if (data == b'!MENU_LIST'):
            #                 print("[SUCCESS] Received menu list")
            #                 menu = json.loads(self.client.recv(1024).decode(FORMAT))
            #                 print(menu)
            #             elif (data == b'!END'):
            #                 index += 1
            #                 break
            #             elif (data == b'!MENU_IMG'):
            #                 f.write(data)
                        

            #         print("[SUCCESS] Received menu image")
            #         return menu
            #     except OSError: 
            #         break

           

    def format_menu(self, menu):
        message = ""
        for item in menu:
            message += f"{item['name']} - {item['price']} VND\n"
        return message

    