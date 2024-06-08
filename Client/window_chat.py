from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import Button, Text, Label
from tkinter import END, UNITS
from time import time, strftime, localtime
import os


class WindowChat(Toplevel):
    def __init__(self):
        super(WindowChat, self).__init__()
        # 设置窗口大小且不可调整
        self.geometry('%dx%d' % (795, 505))
        self.resizable(False, False)

        # 添加组件
        self.add_widget()

        # 语音按钮状态
        self.voice_button_status = False

        # self.on_voice_button_click(lambda: self.change_voice_button_status())

    def add_widget(self):
        # 聊天区
        chat_text_area = ScrolledText(self)
        chat_text_area['width'] = 110
        chat_text_area['height'] = 30
        chat_text_area.grid(row=0, column=0, columnspan=4)
        # 添加两个标签
        chat_text_area.tag_config('green', foreground='#008B00')
        chat_text_area.tag_config('system', foreground='red')
        self.children['chat_text_area'] = chat_text_area

        # 输入区
        chat_input_area = Text(self, name='chat_input_area')
        chat_input_area['width'] = 80
        chat_input_area['height'] = 7
        chat_input_area.grid(row=1, column=0, pady=10)

        # 发送按钮
        send_button = Button(self, name='send_button')
        send_button['width'] = 8
        send_button['height'] = 2
        send_button['text'] = '发送'
        send_button.grid(row=1, column=1)

        # 发送文件按钮
        send_file_button_in_chat = Button(self, name='send_file_button_in_chat')
        send_file_button_in_chat['width'] = 8
        send_file_button_in_chat['height'] = 2
        send_file_button_in_chat['text'] = '发送文件'
        send_file_button_in_chat.grid(row=1, column=2)

        # 语音通话按钮
        voice_button = Button(self, name='voice_button')
        voice_button['width'] = 8
        voice_button['height'] = 2
        voice_button['text'] = '语音通话'
        voice_button.grid(row=1, column=3)

    def set_title(self, title):
        self.title('欢迎 %s 进入聊天室！' % title)

    def on_send_button_click(self, command):
        self.children['send_button']['command'] = command

    def on_send_file_button_in_chat_click(self, command):
        self.children['send_file_button_in_chat']['command'] = command

    def get_inputs(self):
        return self.children['chat_input_area'].get(0.0, END)

    def clear_inputs(self):
        self.children['chat_input_area'].delete(0.0, END)

    def append_message(self, sender, message):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        send_info = '%s: %s\n' % (sender, send_time)
        self.children['chat_text_area'].insert(END, send_info, 'green')
        self.children['chat_text_area'].insert(END, ' ' + message + '\n')

        # 向下滚动
        self.children['chat_text_area'].yview_scroll(3, UNITS)

    def append_file(self, sender, file_name, file_path):
        # 显示发送文件信息，并提供打开链接
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        send_info = '%s: %s\n' % (sender, send_time)
        self.children['chat_text_area'].insert(END, send_info, 'green')
        self.children['chat_text_area'].insert(END, ' 发送文件: %s\n' % file_name)

        # 添加打开链接
        self.children['chat_text_area'].insert(END, ' 点击此处打开文件', 'system')
        self.children['chat_text_area'].tag_bind('system', '<Button-1>', lambda e: self.open_file(file_path))
        self.children['chat_text_area'].insert(END, '\n\n')

        # 向下滚动
        self.children['chat_text_area'].yview_scroll(3, UNITS)

    def on_voice_button_click(self, command):
        self.children['voice_button']['command'] = command

    def set_voice_button_text(self, text):
        self.children['voice_button']['text'] = text
        self.children['voice_button'].update()

    def change_voice_button_status(self):
        if not self.voice_button_status:
            self.voice_button_status = True
            self.set_voice_button_text('关闭语音')
        else:
            self.voice_button_status = False
            self.set_voice_button_text('语音通话')

    def get_voice_button_status(self):
        return self.voice_button_status

    def append_voice(self, sender):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        send_info = '%s: %s\n' % (sender, send_time)
        self.children['chat_text_area'].insert(END, send_info, 'system')
        self.children['chat_text_area'].insert(END, ' ' + '开启了语音通话\n\n')

        # 向下滚动
        self.children['chat_text_area'].yview_scroll(3, UNITS)

    def close_voice(self, sender):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        send_info = '%s: %s\n' % (sender, send_time)
        self.children['chat_text_area'].insert(END, send_info, 'system')
        self.children['chat_text_area'].insert(END, ' ' + '关闭了语音通话\n\n')

        # 向下滚动
        self.children['chat_text_area'].yview_scroll(3, UNITS)

    def open_file(self, file_path):
        os.system('start %s' % file_path)

    def on_window_closed(self, command):
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == '__main__':
    window = WindowChat()
    window.mainloop()
