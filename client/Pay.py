import tkinter as tk
from tkinter.messagebox import showwarning

mess_payment = {
    'method': '',
    'banking_number': ''
}

def Pay(root):
    main_frame = tk.Frame(root)

    check_value = tk.StringVar()
    input_Value = tk.StringVar()

    def displayInput(input, x, y, w, h):
        if (check_value.get() == 'banking'):
            input.place(x=x, y=y, width=w, height=h)
        else:
            input.place(x=x, y=y, width=0, height=0)
    
    def send_mess_payment():
        if (check_value.get() == 'cash'):
            mess_payment['method'] = check_value.get()
            mess_payment['banking_number'] = ''

        elif (check_value.get() == 'banking'):
            if (input_Value.get() == ''):
                showwarning(title='Warning', message='Please, input banking number!')
            else:
                mess_payment['method'] = check_value.get()
                mess_payment['banking_number'] = input_Value.get()
        print(mess_payment) #call function send payload to server

    tk.Checkbutton(main_frame, text="cash on delivery", variable=check_value, onvalue='cash', offvalue='none', command=lambda: displayInput(input_bank, 0, 100, 500, 50)).place(x=0, y=0, width=500, height=50)
    tk.Checkbutton(main_frame, text="pay by card", variable=check_value, onvalue='banking', offvalue='none', command=lambda: displayInput(input_bank, 0, 100, 500, 50)).place(x=0, y=50, width=500, height=50)

    input_bank = tk.Entry(main_frame, textvariable=input_Value)

    tk.Button(main_frame, text='Pay', command=send_mess_payment).place(x = 200, y = 200, width=100, height=50)    
    return main_frame