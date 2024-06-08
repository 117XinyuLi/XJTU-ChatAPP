import tkinter


def test():
    window = tkinter.Tk()

    login_bt = tkinter.Button(window, name='login_bt')
    login_bt['text'] = '登录'
    login_bt.grid(row=0, column=1)

    register_bt = tkinter.Button(window, name='register_bt')
    register_bt['text'] = '注册'
    register_bt.grid(row=0, column=0)

    window.mainloop()


if __name__ == '__main__':
    test()



