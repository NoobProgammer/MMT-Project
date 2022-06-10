from threading import Thread
import tkinter as tk
from tkinter import messagebox
from client import Client

#Client
class App:
    def __init__(self):
        self.client = Client()
        self.client.connect()
        self.window = tk.Tk()
        self.window.title("Restaurant")
        self.window.geometry("400x400")
        self.text_box = tk.Label(self.window, text="")
        self.order_box = tk.Entry(self.window)
        self.order_btn = tk.Button(self.window, text="Order", command=self.make_order)

    def on_receive_menu(self):      
        self.client.request_menu()
        self.text_box.configure(text=self.client.on_receive())

    def make_order(self):
        # Send the menu_id to server
        self.client.make_order(int(self.order_box.get()))
        self.order_box.delete(0, tk.END)
        messagebox.showinfo("Order", "Order successfully")

    def run(self):
        self.text_box.pack()
        self.order_box.pack()
        self.order_btn.pack()

        Thread(target=self.on_receive_menu).start()

        self.window.mainloop()


if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        exit()




