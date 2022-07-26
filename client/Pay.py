from threading import Thread
import tkinter as tk
from tkinter.messagebox import showwarning
from Order import OrderId, setOrderId

mess_payment = {
    'method': '',
    'banking_number': ''
}


def receive_error_msg(on_receive_payment_status):
    error_mess = on_receive_payment_status()
    if(error_mess == "PAYMENT SUCCESSFUL"):
        setOrderId(None)
    print('Err mess: ' + str(error_mess))
    showwarning(title='Warning', message=error_mess)


def Pay(root, make_payment, on_receive_payment_status):
    main_frame = tk.Frame(root)

    check_value = tk.StringVar()
    input_Value = tk.StringVar()

    def displayInput(input, x, y, w, h):
        if (check_value.get() == 'card'):
            input.place(x=x, y=y, width=w, height=h)
        else:
            input.place(x=x, y=y, width=0, height=0)

    def send_mess_payment():
        # validate
        if (check_value.get() == 'cash'):
            mess_payment['method'] = check_value.get()
            mess_payment['banking_number'] = ''
        elif (check_value.get() == 'card'):
            if (input_Value.get() == ''):
                showwarning(title='Warning',
                            message='Please, input banking number!')
            else:
                mess_payment['method'] = check_value.get()
                mess_payment['banking_number'] = input_Value.get()
        else:
            mess_payment['method'] = ''
            mess_payment['banking_number'] = ''

        # send payment method:
        order_id = OrderId()
        if (order_id == None):
            showwarning(title='Warning', message='Let make your order!')
        else:
            if (mess_payment['method'] == ''):
                showwarning(title='Warning',
                            message='Please, choose your payment method!')
            elif (mess_payment['method'] == 'cash'):
                make_payment(order_id, mess_payment['method'])
                Thread(target=lambda: receiveErrorMess(
                    on_receive_payment_status)).start()
            elif (mess_payment['method'] == 'card'):
                make_payment(
                    order_id, mess_payment['method'], mess_payment['banking_number'])
                Thread(target=lambda: receiveErrorMess(
                    on_receive_payment_status)).start()
        # print(mess_payment) #call function send payload to server

    tk.Checkbutton(main_frame, text="cash on delivery", variable=check_value, onvalue='cash', offvalue='none',
                   command=lambda: displayInput(input_bank, 0, 100, 500, 50)).place(x=0, y=0, width=500, height=50)
    tk.Checkbutton(main_frame, text="pay by card", variable=check_value, onvalue='card', offvalue='none',
                   command=lambda: displayInput(input_bank, 0, 100, 500, 50)).place(x=0, y=50, width=500, height=50)

    input_bank = tk.Entry(main_frame, textvariable=input_Value)

    tk.Button(main_frame, text='Pay', command=send_mess_payment).place(
        x=200, y=200, width=100, height=50)
    return main_frame
