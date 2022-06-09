import socket
import json

# MESSAGE
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


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
        self.client.connect(self.addr)

    def send(self, msg):
        message = msg.encode(FORMAT)
        send_length = str(len(message)).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))

        self.client.send(send_length)
        self.client.send(message)

    def on_receive(self):
        while True:
            print("[WAITING] Waiting for response")
            try:
                menu = json.loads(self.client.recv(1024).decode(FORMAT))
                print("[SUCCESS] Received menu")
                return self.format_menu(menu)
            except OSError: 
                break

    def format_menu(self, menu):
        message = ""
        for item in menu:
            message += f"{item['name']} - {item['price']} VND\n"
        return message