import tkinter as tk

def Data(data_menu):
    print(data_menu)
    if (data_menu == None):
        return None
    for item in data_menu:
        item["image"] = tk.PhotoImage(file=item["image"]).subsample(16, 16)
    return data_menu