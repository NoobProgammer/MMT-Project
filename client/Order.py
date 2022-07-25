from cgitb import text
from email.base64mime import header_length
from tkinter import ttk
from tkinter import PhotoImage
from tkinter.messagebox import showwarning
import tkinter as tk
from turtle import heading, width
from unicodedata import name

from pip import main

# cart:
data_order = []
order_id = None

def scroll_frame(main_frame, width):
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    my_scrollbar = ttk.Scrollbar(
        main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
        scrollregion=my_canvas.bbox('all')))

    second_frame = tk.Frame(my_canvas, width=width)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
    return second_frame

def list_item(root, name, id):
    check_value = tk.StringVar()
    quantity_value = tk.StringVar()

    def check_exist(id):
        for item in data_order:
            if (item["id"] == id):
                return True
        return False

    def add_to_cart():
        if(check_value.get() == 'true' and quantity_value.get() != '' and int(quantity_value.get()) > 0):
            if not check_exist(id):
                data_order.append({"id": id, "quantity": int(quantity_value.get())})
            else:
                for item in data_order:
                    if (item["id"] == id):
                        item["quantity"] = quantity_value.get()
            print(data_order)

    wrapper = tk.Frame(root, width=500, height=40)

    checkbox = tk.Checkbutton(
        wrapper, text=name, variable=check_value, onvalue='true', offvalue='false')
    checkbox.place(x=0, y=0, width=350, height=40)

    input_quantity = tk.Entry(wrapper, textvariable=quantity_value)
    input_quantity.place(x=350, y=0, width=50, height=40)

    # add option to cart:
    add_btn = tk.Button(wrapper, text="add to cart", command=add_to_cart)
    add_btn.place(x=400, y=0, width=90, height=40)
    return wrapper

def renderListItem(root, data):
    if (data != None):
        i = 0
        for item in data:
            list_item(root, item["name"], item["id"]).grid(
                row=i, column=0, pady=10, ipadx=5)
            i += 1

def renderOrder(data):
    root = tk.Tk()
    root.title("Your dishes")
    root.geometry("300x500")
    main_frame = scroll_frame(root, 300)
    
    i = 0
    for order in data_order:
        for item in data:
            if (order["id"] == item["id"]):
                tk.Label(main_frame, text=f'{item["name"]} x {order["quantity"]}').grid(row=i, column=0, pady=10, ipadx=5)
                i += 1

    tk.Button(main_frame, text="QUIT", command=root.destroy).grid(row=i+1, column=0)
    data_order.clear()
    root.mainloop()

def handleMakeOrder(make_order, second_frame, data, on_receive_order):
    def handleMoreOrder():
        tk.Frame(second_frame).place(x=0, y=0, width=500, height=700)
        renderListItem(second_frame, data)
    global order_id

    if (len(data_order) == 0):
        showwarning(message='Let choose your dish!')
    else:
        make_order(data_order)
        bill = on_receive_order()
        order_id = bill['id']
        tk.Frame(second_frame).place(x=0, y=0, width=500, height=700)
        tk.Label(second_frame, text="Total price: ", font=('Arial', 17), fg="#ba0c2f").place(x=50, y = 0, width=150, height=50)
        tk.Label(second_frame, text=bill['total_price'], font=('Arial', 17), fg="#ba0c2f").place(x=200, y = 0, height=50)
        tk.Button(second_frame, text="More Order", command=handleMoreOrder).place(x=200, y=50, width=100, height=50)
        renderOrder(data)

# order frame:
def Order(root, data, make_order, on_receive_order):
    # set scroll screen:
    main_frame = tk.Frame(root)
    main_frame.place(x=0, y=50, width=500, height=750)

    # click to order:
    btn_order = tk.Button(main_frame, text="Order", command=lambda: handleMakeOrder(make_order, second_frame, data, on_receive_order))
    btn_order.place(x=200, y=0, width=100, height=50)

    wrap_list = tk.Frame(main_frame)
    wrap_list.place(x=0, y=50, width=500, height=700)
    second_frame = scroll_frame(wrap_list, 500)

    # render list:
    renderListItem(second_frame, data)
    # Return (Order frame, order_btn, order_data)
    return main_frame


def OrderId():
    return order_id