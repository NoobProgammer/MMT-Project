from tkinter import ttk
import tkinter as tk
import Color
import base64

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

def menuItem(frame, img, *arg):
    frameItem = tk.Frame(frame, width=500, height=60)

    #dish image:
    imgLabel = tk.Label(frameItem, image=img)
    imgLabel.place(x=0, y=0, width=60, height=60)
    
    frameInfo = tk.Frame(frameItem, width=500, height=60)
    frameInfo.place(x=60, y=0, width=440, height=60)
    i = 0
    for label in arg:
        tk.Label(frameInfo, text=label, width=400, anchor="w", foreground=Color.color["dark"]).grid(row=i, column=1)
        i += 1
    return frameItem

def Menu(root, data):
    #set scroll screen:
    main_frame = tk.Frame(root)
    main_frame.place(x=0, y=50, width=500, height=750)

    second_frame = scrollFrame(main_frame)
    #render list:
    if (data != None):
        i = 0
        for item in data:
            MenuItem = menuItem(second_frame, item["image"], item["name"], item["price"], item["description"])
            MenuItem.grid(row=i, column=0, pady=10)
            i += 1

    return main_frame


