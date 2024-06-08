from tkinter import Tk
from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import Frame
from tkinter import LEFT
from tkinter import END


class WindowLogin(Tk):
    def __init__(self):
        super(WindowLogin, self).__init__()

        # 设置窗口属性
        self.window_init()

        # 创建控件
        self.add_widget()

    def window_init(self):
        self.title("登录窗口")

        # 设置窗口不能被拉伸
        self.resizable(False, False)

        window_width = 255
        window_height = 95
        self.geometry('%dx%d+%d+%d' % (window_width, window_height,
                                       (self.winfo_screenwidth() - window_width) / 2,
                                       (self.winfo_screenheight() - window_height) / 2))

    def add_widget(self):
        # 用户名
        username_label = Label(self)
        username_label['text'] = '用户名:'
        username_label.grid(row=0, column=0, padx=10, pady=5)

        username_entry = Entry(self, name='username_entry')
        username_entry['width'] = 25
        username_entry.grid(row=0, column=1)

        # 密码
        password_label = Label(self)
        password_label['text'] = '密   码:'
        password_label.grid(row=1, column=0)

        password_entry = Entry(self, name='password_entry')
        password_entry['width'] = 25
        password_entry['show'] = '*'
        password_entry.grid(row=1, column=1)

        # 创建框架
        button_frame = Frame(self, name='button_frame')

        # 重置按钮
        reset_button = Button(button_frame, name='reset_button')
        reset_button['text'] = ' 重置 '
        reset_button.pack(side=LEFT, padx=20)
        # 登录按钮
        login_button = Button(button_frame, name='login_button')
        login_button['text'] = ' 登录 '
        login_button.pack(side=LEFT)

        button_frame.grid(row=2, columnspan=2, pady=5)

    def get_username(self):
        return self.children['username_entry'].get()

    def get_password(self):
        return self.children['password_entry'].get()

    def clear_username(self):
        self.children['username_entry'].delete(0, END)

    def clear_password(self):
        self.children['password_entry'].delete(0, END)

    def on_reset_button_click(self, command):
        reset_button = self.children['button_frame'].children['reset_button']
        reset_button['command'] = command

    def on_login_button_click(self, command):
        login_button = self.children['button_frame'].children['login_button']
        login_button['command'] = command

    def on_window_closed(self, command):
        # 窗口关闭事件
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == '__main__':
    window = WindowLogin()
    window.mainloop()
