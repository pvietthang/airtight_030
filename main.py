from tkinter import *
from tkinter import messagebox,ttk
import serial
import serial.tools.list_ports
import time
import datetime
import requests
import struct
from tkinter import *
import pyautogui as py
import pandas as pd
import traceback
from ERROR import *
file_position = "click_position.csv"
click_pos = pd.read_csv(file_position, index_col=0)
def calibPos():  # chỉnh sửa vị trí click
    def savePos():  # lưu vị trí sau khi chỉnh sửa
        try:
            global click_pos
            list_pos.to_csv(file_position)
            click_pos = pd.read_csv(file_position, index_col=0)
            tk_calib.destroy()
            tk_calib.quit()
        except:
            Systemp_log(traceback.format_exc()).append_new_line()

    def curPos():
        while True:
            try:
                x, y = py.position()
                time.sleep(1)
                if (x, y) == py.position():
                    list_pos.loc[CB_list_pos.get(), 'X'] = x
                    list_pos.loc[CB_list_pos.get(), 'Y'] = y
                    break
            except:
                Systemp_log(traceback.format_exc()).append_new_line()

    try:
        list_pos = pd.read_csv(file_position, index_col=0)
        tk_calib = Toplevel(wk)
        tk_calib.geometry("120x180")
        tk_calib.grab_set()
        tk_calib.resizable(False, False)

        CB_list_pos = ttk.Combobox(tk_calib, state='readonly', font=16, values=pd.read_csv(file_position, index_col=0).index.to_list()[1:])
        CB_list_pos.place(x=5, y=5, width=100, height=30)
        # CB_list_pos.bind("<<ComboBoxSelected>>",curPos)
        btn2 = Button(tk_calib, text="Change", command=curPos, activebackground="red").place(x=5, y=40, width=100, height=30)
        btn5 = Button(tk_calib, text="Save", command=savePos).place(x=5, y=145, width=100, height=30)
        tk_calib.mainloop()
    except:
        Systemp_log(traceback.format_exc()).append_new_line()

meter_ser = serial.Serial(
            port='COM3',
            baudrate=9600,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,

            xonxoff=True
        )
meter_ser.setDTR(True)
meter_ser.setRTS(True)
meter_ser.isOpen()
resulti=""
count=0
time1 = datetime.datetime.now()
def again():
    bytesToRead = meter_ser.inWaiting()
    data = meter_ser.read(bytesToRead)
    b = data
    if len(b)>0:
        print(data)
        py.doubleclick(int(click_pos.loc['Text', 'X']), int(click_pos.loc['Text', 'Y']))
        time.sleep(1)
        py.doubleclick(int(click_pos.loc['Apply', 'X']), int(click_pos.loc['Apply', 'Y']))
        time.sleep(1)
        py.write(data.decode('utf-8').strip())
        time.sleep(1)
        py.press('enter')
    wk.after(1000,again)
wk = Tk()
main_menu = Menu(wk)
wk.configure(menu=main_menu)
edit_menu = Menu(main_menu, tearoff=0)
connect_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Chỉnh Sửa", menu=edit_menu)
edit_menu.add_command(label="Vị Trí Nhấn", command=calibPos)
again()
wk.mainloop()
    