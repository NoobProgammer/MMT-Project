import socket
import threading
import json
import time

# MESSAGE
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


class Server:
    def __init__(self):
        self.ip = '192.168.1.9'
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

    # Handle connection with client
    # conn is the connection
    # addr is the address of the client
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if (msg_length):
                # Get the message length
                msg_length = int(msg_length)
                # Get the actual message
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False

                if (msg == "!INFO"):
                    f = open("menu.json")
                    menu = json.load(f)
                    time.sleep(2)
                    conn.send(json.dumps(menu).encode(FORMAT))
        conn.close()


if __name__ == '__main__':
    server = Server()
    print("[STARTING] server is starting")
    server.start()
