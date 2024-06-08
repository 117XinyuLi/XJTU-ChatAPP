from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import Button, Text, Label
from tkinter import END, UNITS
from time import time, strftime, localtime
import os


class WindowSendFile(Toplevel):
    def __init__(self):
        super(WindowSendFile, self).__init__()

        # 创建发送文件窗口
        self.geometry('380x50')
        self.title('发送文件')
        self.resizable(False, False)

        # 添加组件
        # 文件路径
        file_path_label = Label(self)
        file_path_label['text'] = '文件路径:'
        file_path_label.grid(row=0, column=0, padx=10, pady=5)
        file_path_text = Text(self)
        file_path_text['width'] = 30
        file_path_text['height'] = 1.5
        file_path_text.grid(row=0, column=1, padx=10, pady=5)
        self.children['file_path_text'] = file_path_text

        # 发送按钮
        send_file_button = Button(self, name='send_file_button')
        send_file_button['text'] = '发送'
        send_file_button['width'] = 5
        send_file_button['height'] = 1
        send_file_button.grid(row=0, column=2, padx=10, pady=5)
        self.children['send_file_button'] = send_file_button

        # 点击关闭按钮
        self.on_window_closed(lambda: self.withdraw())

    def on_send_file_button_click(self, command):
        self.children['send_file_button']['command'] = command

    def appear(self):
        self.update()
        self.deiconify()

    def get_file_path_text(self):
        return self.children['file_path_text'].get(0.0, END)

    def clear_file_path_text(self):
        self.children['file_path_text'].delete(0.0, END)

    def on_window_closed(self, command):
        # 点击关闭按钮
        self.protocol('WM_DELETE_WINDOW', command)

