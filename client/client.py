import socket
import json
import threading
import time
from struct import unpack
from datetime import datetime
from tkinter.messagebox import NO

from requests import request
  

# MESSAGE
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
USER_ID = "TABLE001"
# COMMAND
COMMAND_INFO = "!INFO"
COMMAND_ORDER = "!ORDER"
COMMAND_PAYMENT = "!PAYMENT"
COMMAND_EXTEND = "!EXTEND"
COMMAND_EXTRA = "!EXTRA"

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

        is_disconnected = True
        print("[CONNECTING] Connecting to server...")
        while is_disconnected:
            try:
                self.client.connect(self.addr)
                # self.client.settimeout(None)
                is_disconnected = False
                print("[SUCCESS] Connected to server")
            except TimeoutError:
                print("[ERROR] Connection timeout")
                exit()
            except ConnectionRefusedError:
                pass
            except ConnectionAbortedError:
                pass

    def close_connection(self):
        self.client.close()
            
    def encapsulate_request(self, header, data):
        return json.dumps({"header": header, "data": data}).encode(FORMAT)

    def request_menu(self):
        request = self.encapsulate_request(COMMAND_INFO, "")
        self.client.send(request)

    def make_order(self, order):

        order_data = {
            "user_id": USER_ID,
            "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'order': order
        }
        request = self.encapsulate_request(COMMAND_ORDER, order_data)
        self.client.send(request)

          
    def check_expiration(self, order_id):
        request = self.encapsulate_request(COMMAND_EXTEND, order_id)
        self.client.send(request)
        print('[WAITING] Waiting for extend response')
        while True:
            msg = self.client.recv(1024)
            if (msg == b'!EXTEND_TRUE'):
                return 1
            elif (msg == b'!EXTEND_FALSE'):
                return 0
            
    def extend_order(self, order_id, order):
        order_data = {
            'order_id': order_id,
            'order' : order
        }
        request = self.encapsulate_request(COMMAND_EXTRA, order_data)
        self.client.send(request)

    def make_payment(self, order_id, option, card_details = None):
        request = self.encapsulate_request(COMMAND_PAYMENT, {"order_id": order_id, "option": option, "card_details": card_details})
        self.client.send(request)

    def on_receive_payment_status(self):
        print('[WAITING] Waiting for payment status response')
        while True:
            msg = self.client.recv(1024)
            if (msg == b'!PAYMENT_FAIL'):
                failed_msg = "YOUR CARD IS NOT LEGIT, PLEASE REENTER"
                return failed_msg

    def on_receive_order(self):
        print('[WAITING] Waiting for order response')
        total_price = None
        order_id = None
        while True:
            msg = self.client.recv(1024)
            if (msg == b'!ORDER_PRICE'):
                msg = self.client.recv(1024)
                order = json.loads(msg.decode(FORMAT))
                print(order)
                return order
                

        
    def on_receive_menu(self):
        file_index = 1
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
                with open(f"./img/{file_index}.jpg", "wb") as f:
                    while True:
                        msg = self.client.recv(1024)
                        if (msg == b'!END_IMG'):
                            file_index += 1
                            break
                        else:
                            f.write(msg)
            elif(msg == b'!MENU_DONE'):
                print('[DONE] Receiving menu process done')
                return menu

    def format_menu(self, menu):
        message = ""
        for item in menu:
            message += f"{item['name']} - {item['price']} VND\n"
        return message

    