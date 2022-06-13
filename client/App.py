from pickle import NONE
import tkinter as tk
from threading import Thread
import customtkinter as ctk

import Menu
import Order
import Color
from client import Client
# import getData


# class App:
#     def __init__(self):
#         self.client = Client()
#         self.client.connect()
#         self.root = tk.Tk()
#         self.root.title("Tkinter Navbar")
#         self.root.config(bg="gray17")
#         self.root.geometry("500x800")

#     def run(self):
#         self.client.request_menu()
#         Thread(target=self.on_menu_receive).start()
#         self.show_top_navbar()

#         self.root.mainloop()

#     def on_menu_receive(self):
#         data = self.client.on_receive_menu()
#         self.menu_frame = Menu.Menu(self.root, data)
#         self.menu_frame.place(x=0, y=50, width=500, height=750)
#         self.order_frame = Order.Order(self.root, data)
#         self.order_frame.place(x=0, y=50, width=500, height=750)

#     def show_menu_frame(self):
#         self.menu_frame.tkraise()
#         self.menu_btn.config(fg_color=Color.color["main_color"])
#         self.menu_btn.config(hover_color=Color.color["main_color"])
#         self.order_btn.config(fg_color=Color.color["main_color_disabled"])
#         self.order_btn.config(hover_color=Color.color["main_color_disabled"])

#     def show_order_frame(self):
#         self.order_frame.tkraise()
#         self.menu_btn.config(fg_color=Color.color["main_color_disabled"])
#         self.menu_btn.config(hover_color=Color.color["main_color_disabled"])
#         self.order_btn.config(fg_color=Color.color["main_color"])
#         self.order_btn.config(hover_color=Color.color["main_color"])

#     def show_top_navbar(self):
#         self.menu_btn = ctk.CTkButton(master=self.root, text="Menu",
#                                 text_color=Color.color["dark"], 
#                                 fg_color=Color.color["main_color"], 
#                                 hover_color=Color.color["main_color"],
#                                 corner_radius=0, command=self.show_menu_frame)
#         self.menu_btn.place(x=0, y=0, width=250, height=50)
#         self.order_btn = ctk.CTkButton(master=self.root, text="Order", 
#                                 text_color=Color.color["dark"],
#                                 fg_color=Color.color["main_color_disabled"], 
#                                 hover_color=Color.color["main_color_disabled"],
#                                 corner_radius=0, command=self.show_order_frame)
#         self.order_btn.place(x=250, y=0, width=250, height=50)
        

#show frame:
def show_menu_frame():
    menu_frame.tkraise()
    menu_btn.config(fg_color=Color.color["main_color"])
    menu_btn.config(hover_color=Color.color["main_color"])
    order_btn.config(fg_color=Color.color["main_color_disabled"])
    order_btn.config(hover_color=Color.color["main_color_disabled"])

def show_order_frame():
    order_frame.tkraise()
    menu_btn.config(fg_color=Color.color["main_color_disabled"])
    menu_btn.config(hover_color=Color.color["main_color_disabled"])
    order_btn.config(fg_color=Color.color["main_color"])
    order_btn.config(hover_color=Color.color["main_color"])


if __name__ == "__main__":
    # app = App()
    # app.run()

    #create client
    client = Client()
    client.connect()

    # setting root window:
    root = tk.Tk()
    root.title("Tkinter Navbar")
    root.config(bg="gray17")
    root.geometry("500x800")

    # top Navigation bar:
    menu_btn = ctk.CTkButton(master=root, text="Menu", 
                            text_color=Color.color["dark"], 
                            fg_color=Color.color["main_color"], 
                            hover_color=Color.color["main_color"],
                            corner_radius=0, command=show_menu_frame)
    menu_btn.place(x=0, y=0, width=250, height=50)

    order_btn = ctk.CTkButton(master=root, text="Order", 
                            text_color=Color.color["dark"],
                            fg_color=Color.color["main_color_disabled"], 
                            hover_color=Color.color["main_color_disabled"],
                            corner_radius=0, command=show_order_frame)
    order_btn.place(x=250, y=0, width=250, height=50)

    #get data from server:
    client.request_menu()
    data = client.on_receive_menu()
    #data = getData.Data(dataMenu)

    #order frame
    order_frame = Order.Order(root, data, client.make_order)
    order_frame.place(x=0, y=50, width=500, height=750)

    #menu frame
    menu_frame = Menu.Menu(root, data)
    menu_frame.place(x=0, y=50, width=500, height=750)

    # window in mainloop:
    root.mainloop()
