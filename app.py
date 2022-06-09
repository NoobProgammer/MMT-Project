from threading import Thread
import tkinter as tk

from requests import request
from client.client import Client

#Client
class App:
    def __init__(self):
        self.client = Client()
        self.client.connect()
        self.window = tk.Tk()
        self.window.title("Restaurant")
        self.window.geometry("400x400")
        self.text_box = tk.Label(self.window, text="")

    def run(self):
        self.text_box.pack()
        Thread(target=self.on_receive_menu).start()
        self.window.mainloop()

    def on_receive_menu(self):
        # Send request to server        
        self.client.send("!INFO")
        self.text_box.configure(text=self.client.on_receive())


if __name__ == "__main__":
    app = App()
    app.run()




