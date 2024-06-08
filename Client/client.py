from tkinter.messagebox import showinfo
from window_login import WindowLogin
from request_protocol import RequestProtocol
from client_socket import ClientSocket
from threading import Thread
from config import *
from window_chat import WindowChat
from window_send_file import WindowSendFile
import sys
import os
import pyaudio
import socket


class Client:
    def __init__(self):
        # 初始化客户端套接字
        self.conn = ClientSocket()

        # 初始化登录窗口
        self.window = WindowLogin()
        self.window.on_reset_button_click(self.clear_inputs)
        self.window.on_login_button_click(self.send_login_data)
        self.window.on_window_closed(self.exit)

        # 初始化发送文件窗口
        self.window_send_file = WindowSendFile()
        self.window_send_file.withdraw()
        self.window_send_file.on_send_file_button_click(self.send_file_data)

        # 初始化聊天窗口
        self.window_chat = WindowChat()
        self.window_chat.withdraw()
        self.window_chat.on_send_button_click(self.send_chat_data)
        self.window_chat.on_send_file_button_in_chat_click(self.window_send_file.appear)
        self.window_chat.on_voice_button_click(lambda: self.process_voice())
        self.window_chat.on_window_closed(self.exit)



        # 初始化消息处理函数
        self.response_handle_function = dict()
        self.register(RESPONSE_LOGIN_RESULT, self.response_login_handle)
        self.register(RESPONSE_CHAT, self.response_chat_handle)
        self.register(RESPONSE_SEND_FILE, self.response_send_file_handle)
        self.register(RESPONSE_AUDIO_SETTING, self.response_audio_setting_handle)
        self.register(RESPONSE_AUDIO_CLOSE, self.response_audio_close_handle)

        # 用户名
        self.username = None

        # 程序退出标志
        self.is_running = True

        # 文件嵌套字
        self.file_socket = None

        # 文件保存路径
        self.file_path = None

        # 音频
        self.ip = None
        self.port = None
        self.get_audio_setting = False
        self.is_audio = True
        self.audio_socket = None
        self.playing_stream = None
        self.recording_stream = None
        self.pyaudio = None
        self.receive_thread = None
        self.send_thread = None


    def register(self, response_id, handle_function):
        self.response_handle_function[response_id] = handle_function

    def startup(self):
        # 连接服务器
        self.conn.connect(SERVER_IP, SERVER_PORT)

        Thread(target=self.response_handle).start()
        self.window.mainloop()

    def clear_inputs(self):
        self.window.clear_username()
        self.window.clear_password()

    def send_login_data(self):
        # 获取用户名和密码
        username = self.window.get_username()
        password = self.window.get_password()

        # 生成协议文本
        request_text = RequestProtocol.request_login_result(username, password)
        print(request_text)

        # 发送到服务器
        self.conn.send_data(request_text)

    def response_handle(self):
        while self.is_running:
            # 接收服务器数据
            recv_data = self.conn.recv_data()
            print('Received:', recv_data)

            # 解析数据
            response_data = self.parse_response_data(recv_data)

            # 分析数据并调用相应的函数
            handle_function = self.response_handle_function.get(response_data['response_id'])
            if not handle_function == self.response_audio_setting_handle and not handle_function == self.response_audio_close_handle and not self.response_send_file_handle:
                handle_function(response_data)
            else:
                Thread(target=handle_function, args=(response_data,)).start()

    @staticmethod
    def parse_response_data(recv_data):
        """解析两类数据：登录结果和聊天结果"""
        response_data_list = recv_data.split(DELIMITER)
        response_data = dict()
        response_data['response_id'] = response_data_list[0]
        if response_data['response_id'] == RESPONSE_LOGIN_RESULT:
            response_data['result'] = response_data_list[1]
            response_data['nickname'] = response_data_list[2]
            response_data['username'] = response_data_list[3]
        elif response_data['response_id'] == RESPONSE_CHAT:
            response_data['nickname'] = response_data_list[1]
            response_data['message'] = response_data_list[2]
        elif response_data['response_id'] == RESPONSE_SEND_FILE:
            response_data['nickname'] = response_data_list[1]
            response_data['file_name'] = response_data_list[2]
        elif response_data['response_id'] == RESPONSE_AUDIO_SETTING:
            response_data['nickname'] = response_data_list[1]
            response_data['ip'] = response_data_list[2]
            response_data['port'] = response_data_list[3]
        elif response_data['response_id'] == RESPONSE_AUDIO_CLOSE:
            response_data['nickname'] = response_data_list[1]

        return response_data

    def response_login_handle(self, response_data):
        print('response_login_handle:', response_data)
        result = response_data['result']
        if result == '0':
            showinfo('提示', '登录失败, 用户名或密码错误')
            print('登录失败')
            return

        showinfo('提示', '登录成功')
        nickname = response_data['nickname']
        self.username = response_data['username']
        self.file_path = os.path.join(FILE_PATH, self.username)
        # 如果文件夹不存在则创建
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

        print('登录成功', nickname, self.username)

        # 显示聊天窗口
        self.window_chat.set_title(nickname)
        self.window_chat.update()
        self.window_chat.deiconify()

        # 隐藏登录窗口
        self.window.withdraw()

    def response_chat_handle(self, response_data):
        print('response_chat_handle:', response_data)
        sender = response_data['nickname']
        message = response_data['message']
        self.window_chat.append_message(sender, message)

    def send_chat_data(self):
        # 获取聊天信息
        message = self.window_chat.get_inputs()
        self.window_chat.clear_inputs()

        # 生成协议文本
        request_text = RequestProtocol.request_chat(self.username, message)
        print(request_text)

        # 发送到服务器
        self.conn.send_data(request_text)

        # 显示到聊天窗口
        self.window_chat.append_message('我', message)

    def send_file_data(self):
        # 选择文件
        send_file_path = self.window_send_file.get_file_path_text()
        print('send_file_path:', send_file_path)
        send_file_path = send_file_path.strip()
        send_file_path = send_file_path.replace('\n', '')
        self.window_send_file.clear_file_path_text()
        if not send_file_path:
            showinfo('提示', '请选择文件')
            return
        if not os.path.exists(send_file_path):
            showinfo('提示', '文件不存在')
            return

        # 发送文件信息
        request_text = RequestProtocol.request_send_file(self.username, os.path.basename(send_file_path))
        print(request_text)

        # 发送到服务器
        self.conn.send_data(request_text)

        # 连接服务器并发送文件
        self.file_socket = ClientSocket()
        while True:
            try:
                self.file_socket.connect(SERVER_IP, FILE_PORT)
                break
            except:
                pass
        print('Connected to server file port:', FILE_PORT)

        self.file_socket.send_file(send_file_path)

        # 显示到聊天窗口
        self.window_chat.append_file('我', os.path.basename(send_file_path), send_file_path)

        # 关闭发送文件窗口
        self.window_send_file.withdraw()

        self.file_socket.close()

    def response_send_file_handle(self, response_data):
        print('response_send_file_handle:', response_data)
        sender = response_data['nickname']
        file_name = response_data['file_name']
        file_path = os.path.join(self.file_path, file_name)

        # 连接服务器并接收文件
        self.file_socket = ClientSocket()
        while True:
            try:
                self.file_socket.connect(SERVER_IP, FILE_PORT)
                break
            except:
                pass
        print('Connected to server file port:', FILE_PORT)

        self.file_socket.recv_file(file_path)

        # 显示到聊天窗口，并且可以点击文件名打开文件
        self.window_chat.append_file(sender, file_name, file_path)

        self.file_socket.close()

    def response_audio_setting_handle(self, response_data):
        print('response_audio_setting_handle:', response_data)
        nickname = response_data['nickname']
        self.ip = response_data['ip']
        self.port = int(response_data['port'])
        if self.window_chat.get_voice_button_status():
            self.get_audio_setting = True
        if not self.window_chat.get_voice_button_status():
            self.window_chat.append_voice(nickname)
            self.window_chat.change_voice_button_status()
            self.start_voice()

    def response_audio_close_handle(self, response_data):
        print('response_audio_close_handle:', response_data)
        nickname = response_data['nickname']
        self.window_chat.close_voice(nickname)
        if self.window_chat.get_voice_button_status():
            self.window_chat.change_voice_button_status()
            self.stop_voice()

    def process_voice(self):
        self.window_chat.change_voice_button_status()
        if self.window_chat.get_voice_button_status():
            print('Start voice')
            msg = RequestProtocol.request_audio_setting(self.username)
            self.conn.send_data(msg)
            while not self.get_audio_setting:
                pass
            self.get_audio_setting = False
            self.window_chat.append_voice('我')
            self.start_voice()
        else:
            print('Close voice')
            msg = RequestProtocol.request_audio_close(self.username)
            self.conn.send_data(msg)
            self.window_chat.close_voice('我')
            self.stop_voice()

    def start_voice(self):
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket.connect((self.ip, self.port))
        print(self.ip, self.port)
        self.pyaudio = pyaudio.PyAudio()
        self.playing_stream = self.pyaudio.open(format=audio_format, channels=channels, rate=rate, output=True,
                                                frames_per_buffer=chunk_size)
        self.recording_stream = self.pyaudio.open(format=audio_format, channels=channels, rate=rate, input=True,
                                                  frames_per_buffer=chunk_size)

        self.is_audio = True
        self.receive_thread = Thread(target=self.receive_server_data)
        self.receive_thread.start()
        self.send_thread = Thread(target=self.send_data_to_server)
        self.send_thread.start()
        print('Start audio')

    def stop_voice(self):
        self.is_audio = False
        if self.audio_socket:
            self.audio_socket.close()
            self.audio_socket = None
        if self.pyaudio:
            self.pyaudio.terminate()
            self.pyaudio = None
        if self.playing_stream:
            self.playing_stream.close()
            self.playing_stream = None
        if self.recording_stream:
            self.recording_stream.close()
            self.recording_stream = None
        if self.send_thread:
            self.send_thread.join()
            self.send_thread = None
        if self.receive_thread:
            self.receive_thread.join()
            self.receive_thread = None
        self.is_audio = True
        print('Close audio')

    def receive_server_data(self):
        while self.is_audio:
            try:
                data = self.audio_socket.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while self.is_audio:
            try:
                data = self.recording_stream.read(1024)
                self.audio_socket.sendall(data)
            except:
                pass

    def exit(self):
        self.is_running = False
        self.conn.close()
        sys.exit(0)


if __name__ == '__main__':
    client = Client()
    client.startup()
