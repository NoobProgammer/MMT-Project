
import tkinter as tk
import customtkinter as ctk
import Menu
import Order
import Pay
import Color
import getData
from client import Client

# show frame:


def show_menu_frame():
    menu_frame.tkraise()
    menu_btn.config(fg_color=Color.color["main_color"])
    menu_btn.config(hover_color=Color.color["main_color"])
    order_btn.config(fg_color=Color.color["main_color_disabled"])
    order_btn.config(hover_color=Color.color["main_color_disabled"])
    pay_btn.config(fg_color=Color.color["main_color_disabled"])
    pay_btn.config(hover_color=Color.color["main_color_disabled"])


def show_order_frame():
    order_frame.tkraise()
    order_btn.config(fg_color=Color.color["main_color"])
    order_btn.config(hover_color=Color.color["main_color"])
    menu_btn.config(fg_color=Color.color["main_color_disabled"])
    menu_btn.config(hover_color=Color.color["main_color_disabled"])
    pay_btn.config(fg_color=Color.color["main_color_disabled"])
    pay_btn.config(hover_color=Color.color["main_color_disabled"])


def show_pay_frame():
    pay_frame.tkraise()
    pay_btn.config(fg_color=Color.color["main_color"])
    pay_btn.config(hover_color=Color.color["main_color"])
    menu_btn.config(fg_color=Color.color["main_color_disabled"])
    menu_btn.config(hover_color=Color.color["main_color_disabled"])
    order_btn.config(fg_color=Color.color["main_color_disabled"])
    order_btn.config(hover_color=Color.color["main_color_disabled"])


def receive_menu():
    while True:
        global data
        global menu_frame
        global order_frame
        dataMenu = client.on_receive_menu()
        data = getData.Data(dataMenu)
        order_frame = Order.Order(
            root, data, client.make_order, client.on_receive_order)
        menu_frame = Menu.Menu(root, data)
        show_menu_frame()


if __name__ == "__main__":
    # Create client
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
    menu_btn.place(x=0, y=0, width=166, height=50)

    order_btn = ctk.CTkButton(master=root, text="Order",
                              text_color=Color.color["dark"],
                              fg_color=Color.color["main_color_disabled"],
                              hover_color=Color.color["main_color_disabled"],
                              corner_radius=0, command=show_order_frame)
    order_btn.place(x=166, y=0, width=166, height=50)

    pay_btn = ctk.CTkButton(master=root, text="Pay",
                            text_color=Color.color["dark"],
                            fg_color=Color.color["main_color_disabled"],
                            hover_color=Color.color["main_color_disabled"],
                            corner_radius=0, command=show_pay_frame)
    pay_btn.place(x=332, y=0, width=166, height=50)

    data = None
    # Send a menu request
    client.request_menu()
    dataMenu = client.on_receive_menu()
    data = getData.Data(dataMenu)

    # pay frame
    pay_frame = Pay.Pay(root, client.make_payment,
                        client.on_receive_payment_status)
    pay_frame.place(x=0, y=50, width=500, height=750)

    # order frame
    order_frame = Order.Order(root, data, client.make_order,
                              client.on_receive_order, client.check_expiration, client.extend_order)
    order_frame.place(x=0, y=50, width=500, height=750)

    # Menu frame:
    menu_frame = Menu.Menu(root, data)
    menu_frame.place(x=0, y=50, width=500, height=750)

    # Window in mainloop:
    root.mainloop()
