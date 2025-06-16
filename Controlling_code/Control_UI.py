import numpy as np
import serial
import time
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from threading import Thread


def send_serial_command(PFC, value, port):
    STX = '!'
    ID_1 = '1'
    ID_0 = '6'
    AI = '0'

    # Separate the tens and ones digits
    tens = PFC // 10
    ones = PFC % 10
    PFC_1 = str(tens)
    PFC_0 = str(ones)

    # Separate the individual digits
    letters = list(value)

    Value_5 = letters[0]
    Value_4 = letters[1]
    Value_3 = letters[2]
    Value_2 = letters[3]
    Value_1 = letters[4]
    Value_0 = letters[5]

    # Convert the ASCII characters to byte values
    data_bytes = np.array([ord(STX), ord(ID_1), ord(ID_0), ord(AI), ord(PFC_1), ord(PFC_0),
                           ord(Value_5), ord(Value_4), ord(Value_3), ord(Value_2), ord(Value_1), ord(Value_0)])

    # Calculate the CRC
    crc = np.fmod(np.sum(data_bytes), 256)

    # Convert the CRC to a 3-byte ASCII representation
    crc_ascii = '{:03d}'.format(crc)

    # Combine the pump input command
    message = "b'" + STX + ID_1 + ID_0 + AI + PFC_1 + PFC_0 + Value_5 + Value_4 + Value_3 + Value_2 + Value_1 + Value_0 + crc_ascii + "\n'"
    port.write(message.encode('utf-8'))


def send_command_to_port1():
    PFC = int(entry_pfc_port1.get())
    value = entry_value_port1.get()
    send_serial_command(PFC, value, port1)


def send_command_to_port2():
    PFC = int(entry_pfc_port2.get())
    value = entry_value_port2.get()
    send_serial_command(PFC, value, port2)


def send_command_to_port3():
    PFC = int(entry_pfc_port3.get())
    value = entry_value_port3.get()
    send_serial_command(PFC, value, port3)


def read_data(port):
    # 读取16字节
    au = port.read(16)
    if len(au) != 16:
        print("Error: Invalid response length")
        return None

    # 判断是否为错误返回
    if au == b'NACK':
        print("Error: NACK received")
        return None
    return au


def start_reading_data():
    port3.write(b'!51017000000063\n')
    port3.write(b'!51018000001065\n')
    port3.write(b'!51090000000064\n')
    # 初始化一个空的DataFrame
    data = pd.DataFrame(columns=['AU'])

    # 获取用户输入的停止记录时长，并转换为秒
    stop_time_duration = int(stop_time_duration_entry.get()) * 60

    # 设置循环停止时间
    stop_time = time.time() + stop_time_duration
    while time.time() < stop_time:
        au = read_data(port3)
        if au is not None:
            data = data.append({'AU': au}, ignore_index=True)

    # 保存数据到Excel文件
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"
    data.to_excel(filename, index=False)


if __name__ == '__main__':
    port1 = serial.Serial("COM10", 9600, timeout=None)
    port2 = serial.Serial("COM11", 9600, timeout=None)
    port3 = serial.Serial("COM13", 9600, timeout=None)

    # 创建主窗口
    root = tk.Tk()
    root.title("Serial Command Sender")

    # 创建表格布局
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # 输入框和按钮：Port1
    ttk.Label(mainframe, text="Port1: COM10").grid(column=1, row=1, sticky=tk.W)
    entry_pfc_port1 = ttk.Entry(mainframe, width=7)
    entry_pfc_port1.grid(column=2, row=1, sticky=(tk.W, tk.E))
    entry_value_port1 = ttk.Entry(mainframe, width=7)
    entry_value_port1.grid(column=3, row=1, sticky=(tk.W, tk.E))
    ttk.Button(mainframe, text="Send Command", command=send_command_to_port1).grid(column=4, row=1, sticky=tk.W)

    # 输入框和按钮：Port2
    ttk.Label(mainframe, text="Port2: COM11").grid(column=1, row=2, sticky=tk.W)
    entry_pfc_port2 = ttk.Entry(mainframe, width=7)
    entry_pfc_port2.grid(column=2, row=2, sticky=(tk.W, tk.E))
    entry_value_port2 = ttk.Entry(mainframe, width=7)
    entry_value_port2.grid(column=3, row=2, sticky=(tk.W, tk.E))
    ttk.Button(mainframe, text="Send Command", command=send_command_to_port2).grid(column=4, row=2, sticky=tk.W)

    # 输入框和按钮：Port3
    ttk.Label(mainframe, text="Port3: COM13").grid(column=1, row=3, sticky=tk.W)
    entry_pfc_port3 = ttk.Entry(mainframe, width=7)
    entry_pfc_port3.grid(column=2, row=3, sticky=(tk.W, tk.E))
    entry_value_port3 = ttk.Entry(mainframe, width=7)
    entry_value_port3.grid(column=3, row=3, sticky=(tk.W, tk.E))
    ttk.Button(mainframe, text="Send Command", command=send_command_to_port3).grid(column=4, row=3, sticky=tk.W)

    stop_time_duration_entry = ttk.Entry(mainframe, width=7)
    stop_time_duration_entry.grid(column=3, row=4, sticky=(tk.W, tk.E))

    ttk.Label(mainframe, text="Enter stop time duration (in minutes):").grid(column=2, row=4, sticky=tk.E)

    ttk.Button(mainframe, text="Start Reading Data", command=start_reading_data).grid(column=4, row=4, sticky=tk.W)
    # 循环遍历所有子部件，设置它们的内边距
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # 设置焦点
    entry_pfc_port1.focus()

    # 运行主循环
    root.mainloop()

    # 关闭端口
    port1.write(b'!16016000000063\n')
    port1.close()
    port2.write(b'!16016000000063\n')
    port2.close()

    port3.close()


