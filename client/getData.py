from PIL import Image, ImageTk

def Data(dataMenu):
    print(dataMenu)
    if (dataMenu == None):
        return None
    for item in dataMenu:
        image = Image.open(item["image"])
        image = image.resize((100, 100), Image.ANTIALIAS)
        item["image"] = ImageTk.PhotoImage(image)
    return dataMenu