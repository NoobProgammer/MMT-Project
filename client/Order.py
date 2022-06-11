from tkinter import ttk
from tkinter import PhotoImage
import tkinter as tk

#cart:
dataOrder = []

def scrollFrame(main_frame):
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT ,fill=tk.BOTH, expand=True)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

    second_frame = tk.Frame(my_canvas, width=500)
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    return second_frame

#option to order:
def listItem(root, name, id):
    checkValue = tk.StringVar()
    quantityValue = tk.StringVar()

    def checkExist(id):
        for item in dataOrder:
            if id in item.keys():
                return True
        return False

    def addToCart():
        if(checkValue.get() == 'true' and quantityValue.get() != '' and int(quantityValue.get()) > 0):
            if not checkExist(id):
                dataOrder.append({id: quantityValue.get()})
            else:
                for item in dataOrder:
                    if id in item.keys():
                        item[id] = quantityValue.get()
            print(dataOrder)

    wrapper = tk.Frame(root, width=500, height=40)

    checkbox = tk.Checkbutton(wrapper, text=name, variable=checkValue, onvalue='true', offvalue='false')
    checkbox.place(x=0, y=0, width=350, height=40)

    inputQuantity = tk.Entry(wrapper, textvariable=quantityValue)
    inputQuantity.place(x=350, y=0, width=50, height=40)

    #add option to cart:
    addBtn = tk.Button(wrapper, text="add to cart", command=addToCart)
    addBtn.place(x=400, y=0, width=90, height=40)
    return wrapper

#order frame:
def Order(root, data):
    #set scroll screen:
    main_frame = tk.Frame(root)
    main_frame.place(x=0, y=50, width=500, height=750)

    #click to order:
    btnOrder = tk.Button(main_frame, text="Order", command=lambda: print(dataOrder))
    btnOrder.place(x=0, y=0, width=100, height=50)

    wrapList = tk.Frame(main_frame)
    wrapList.place(x=0, y=50, width=500, height=700)
    second_frame = scrollFrame(wrapList)

    #render list:
    i = 0
    for item in data:
        listItem(second_frame, item["name"], item["id"]).grid(row=i, column=0, pady=10, ipadx=5)
        i += 1
    return main_frame
