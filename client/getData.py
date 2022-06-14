import tkinter as tk
import time

def Data(dataMenu):
    print(dataMenu)
    if (dataMenu == None):
        return None
    for item in dataMenu:
        item["image"] = tk.PhotoImage(file=item["image"]).subsample(16, 16)
    return dataMenu