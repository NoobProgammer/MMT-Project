import tkinter as tk
import customtkinter as ctk
from threading import Thread

import Menu
import Order
import Color
import getData
from client import Client

#create client
client = Client()
client.connect()

# setting root window:
root = tk.Tk()
root.title("Tkinter Navbar")
root.config(bg="gray17")
root.geometry("500x800")

#show frame:
def showMenuFrame():
    menuFrame.tkraise()
    menuBtn.config(fg_color=Color.color["main_color"])
    menuBtn.config(hover_color=Color.color["main_color"])
    orderBtn.config(fg_color=Color.color["main_color_disabled"])
    orderBtn.config(hover_color=Color.color["main_color_disabled"])

def showOrderFrame():
    orderFrame.tkraise()
    menuBtn.config(fg_color=Color.color["main_color_disabled"])
    menuBtn.config(hover_color=Color.color["main_color_disabled"])
    orderBtn.config(fg_color=Color.color["main_color"])
    orderBtn.config(hover_color=Color.color["main_color"])

# top Navigation bar:
menuBtn = ctk.CTkButton(master=root, text="Menu", 
                        text_color=Color.color["dark"], 
                        fg_color=Color.color["main_color"], 
                        hover_color=Color.color["main_color"],
                        corner_radius=0, command=showMenuFrame)
menuBtn.place(x=0, y=0, width=250, height=50)

orderBtn = ctk.CTkButton(master=root, text="Order", 
                        text_color=Color.color["dark"],
                        fg_color=Color.color["main_color_disabled"], 
                        hover_color=Color.color["main_color_disabled"],
                        corner_radius=0, command=showOrderFrame)
orderBtn.place(x=250, y=0, width=250, height=50)

#get data from server:
client.request_menu()
data = client.on_receive_menu()
#data = getData.Data(dataMenu)

#order frame
orderFrame = Order.Order(root, data)
orderFrame.place(x=0, y=50, width=500, height=750)

#menu frame
menuFrame = Menu.Menu(root, data)
menuFrame.place(x=0, y=50, width=500, height=750)

# window in mainloop:
root.mainloop()