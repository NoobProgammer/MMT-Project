import tkinter as tk

def Data(dataMenu):
    print(dataMenu)
    for item in dataMenu:
        item["image"] = tk.PhotoImage(file=item["image"]).subsample(10, 10)
    return dataMenu