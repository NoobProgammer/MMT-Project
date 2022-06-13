from tkinter import ttk
from tkinter import PhotoImage
import tkinter as tk

from pip import main

# cart:
data_order = []


def scroll_frame(main_frame):
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    my_scrollbar = ttk.Scrollbar(
        main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
        scrollregion=my_canvas.bbox('all')))

    second_frame = tk.Frame(my_canvas, width=500)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
    return second_frame

# option to order:


def list_item(root, name, id):
    check_value = tk.StringVar()
    quantity_value = tk.StringVar()

    def check_exist(id):
        for item in data_order:
            if id in item.keys():
                return True
        return False

    def add_to_cart():
        if(check_value.get() == 'true' and quantity_value.get() != '' and int(quantity_value.get()) > 0):
            if not check_exist(id):
                data_order.append({"id": id,
                                  "quantity": int(quantity_value.get())})
            else:
                for item in data_order:
                    if id in item.keys():
                        item[id] = quantity_value.get()
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

# order frame:


def Order(root, data, make_order):
    # set scroll screen:
    main_frame = tk.Frame(root)
    main_frame.place(x=0, y=50, width=500, height=750)

    # click to order:
    btn_order = tk.Button(main_frame, text="Order", command=lambda: make_order(data_order))
    btn_order.place(x=0, y=0, width=100, height=50)

    tk.Label(main_frame, text="Total price: ").place(x=120, y = 0, width=80, height=50)

    #get total price from server:
    total_price = 0 #call function getting total price from server
    tk.Label(main_frame, text=total_price).place(x=195, y = 0, height=50)


    wrap_list = tk.Frame(main_frame)
    wrap_list.place(x=0, y=50, width=500, height=700)
    second_frame = scroll_frame(wrap_list)

    # render list:
    if (data != None):
        i = 0
        for item in data:
            list_item(second_frame, item["name"], item["id"]).grid(
                row=i, column=0, pady=10, ipadx=5)
            i += 1
    # Return (Order frame, order_btn, order_data)
    return main_frame
