from server_socket import ServerSocket
from socket_wrapper import SocketWrapper
from threading import Thread
from config import *
from response_protocol import *
from DB import DB
import os
import psutil
import socket


def get_ip_address(interface_name):
    addresses = psutil.net_if_addrs()
    if interface_name in addresses:
        for address in addresses[interface_name]:
            if address.family == socket.AF_INET:
                return address.address
    return None


class Server(object):
    def __init__(self):
        self.server_socket = ServerSocket()
        self.request_handle_func = {}
        self.register_request_handle_func(REQUEST_LOGIN, self.request_login_handle)
        self.register_request_handle_func(REQUEST_CHAT, self.request_chat_handle)
        self.register_request_handle_func(REQUEST_SEND_FILE, self.request_send_file_handle)
        self.register_request_handle_func(REQUEST_AUDIO_SETTING, self.request_audio_setting_handle)
        self.register_request_handle_func(REQUEST_AUDIO_CLOSE, self.request_audio_close_handle)

        # 创建保存当前登录用户的字典
        self.clients = {}

        # 创建DB
        self.db = DB()

        # 文件socket
        self.file_socket = None

        # 创建线程集合
        self.thread_set = []

        # 音频
        self.audio_clients = []
        self.audio_socket = None
        self.audio_ip = None
        self.audio_thread = None

        # 是否开启音频
        self.set_audio = True

    def register_request_handle_func(self, request_id, handle_func):
        self.request_handle_func[request_id] = handle_func

    def startup(self):
        """Start up the server"""
        while True:
            # 获取客户端连接
            print('Waiting for connection...')
            soc, addr = self.server_socket.accept()
            print('Connected by', addr)

            # 收发数据
            socket_wrapper = SocketWrapper(soc)
            t = Thread(target=self.request_handle, args=(socket_wrapper,))
            t.start()

    def request_handle(self, socket_wrapper: SocketWrapper):
        """Handle the request from client"""
        while True:
            # 接收客户端数据
            data = socket_wrapper.recv_data()
            if data:
                print('Received:', data)
            if not data:
                print('Connection closed')
                self.remove_offline_user(socket_wrapper)
                socket_wrapper.close()
                break

            # 解析数据
            parse_data = self.parse_request_text(data)
            print('Parse data:', parse_data)

            # 分析数据并调用相应的函数
            handle_function = self.request_handle_func.get(parse_data['request_id'])
            if handle_function:
                if handle_function == self.request_audio_setting_handle:
                    self.audio_thread = Thread(target=handle_function, args=(socket_wrapper, parse_data,))
                    self.audio_thread.start()
                elif handle_function == self.request_send_file_handle:
                    Thread(target=handle_function, args=(socket_wrapper, parse_data,)).start()
                else:
                    handle_function(socket_wrapper, parse_data)

    def remove_offline_user(self, socket_wrapper: SocketWrapper):
        """Remove the offline user"""
        print('Remove the offline user')
        for username, client in self.clients.items():
            if client['sock'] == socket_wrapper:
                print('Remove user:', username)
                del self.clients[username]
                break

    def parse_request_text(self, text):
        print('Parse the request text:', text)
        """
        登录信息：0001|用户名|密码
        聊天信息：0002|用户名|消息
        发送文件：0003|用户名|文件名
        语音设置：0004|用户名
        语音关闭：0005|用户名
        """
        request_list = text.split(DELIMITER)
        # 按照类型解析数据
        request_data = {}
        request_data['request_id'] = request_list[0]
        if request_data['request_id'] == REQUEST_LOGIN:
            request_data['username'] = request_list[1]
            request_data['password'] = request_list[2]
        elif request_data['request_id'] == REQUEST_CHAT:
            request_data['username'] = request_list[1]
            request_data['message'] = request_list[2]
        elif request_data['request_id'] == REQUEST_SEND_FILE:
            request_data['username'] = request_list[1]
            request_data['file_name'] = request_list[2]
        elif request_data['request_id'] == REQUEST_AUDIO_SETTING:
            request_data['username'] = request_list[1]
        elif request_data['request_id'] == REQUEST_AUDIO_CLOSE:
            request_data['username'] = request_list[1]

        return request_data

    def request_login_handle(self, client_soc: SocketWrapper, request_data: dict):
        # 获取账号密码
        username = request_data['username']
        password = request_data['password']

        # 验证账号密码
        ret, nickname, username = self.check_user_login(username, password)

        # 登录成功则需要保存用户信息
        if ret == '1':
            print('Login success')
            # 保存用户信息
            self.clients[username] = {'sock': client_soc, 'nickname': nickname}

        # 生成返回信息
        response_text = ResponseProtocol.response_login_result(ret, nickname, username)

        # 发送返回信息
        client_soc.send_data(response_text)

    def request_chat_handle(self, client_soc: SocketWrapper, request_data: dict):
        print('Request chat handle')

        username = request_data['username']
        messages = request_data['message']
        nickname = self.clients[username]['nickname']

        # 拼接返回信息
        msg = ResponseProtocol.response_chat(nickname, messages)

        # 发送返回信息
        for u_name, client in self.clients.items():
            if u_name == username:
                continue
            client['sock'].send_data(msg)

    def request_send_file_handle(self, client_soc: SocketWrapper, request_data: dict):
        print('Request send file handle')

        username = request_data['username']
        file_name = request_data['file_name']
        nickname = self.clients[username]['nickname']

        # 接收文件
        file_path = os.path.join(FILE_PATH, file_name)

        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_socket.bind((SERVER_IP, FILE_PORT))
        self.file_socket.listen(100)
        print('file running on IP: ' + SERVER_IP)

        file_client, addr = self.file_socket.accept()
        file_client_wrapper = SocketWrapper(file_client)
        file_client_wrapper.recv_file(file_path)
        print('Received file:', file_name)

        # 拼接返回信息
        msg = ResponseProtocol.response_send_file(nickname, file_name)

        # 发送返回信息与文件
        for u_name, client in self.clients.items():
            if u_name == username:
                continue
            client['sock'].send_data(msg)
            # client['sock'].send_file(file_path)
            file_client, addr = self.file_socket.accept()
            file_client_wrapper = SocketWrapper(file_client)
            file_client_wrapper.send_file(file_path)
            print('Send file:', file_name)

        self.file_socket.close()
        print('Close file socket')

    def check_user_login(self, username, password):
        # 查询数据库
        result = self.db.get_one("select * from users where user_name='%s'" % username)
        # 模拟返回数据
        if not result:
            return '0', '', username

        # 检查密码
        if result['user_password'] != password:
            return '0', '', username

        return '1', result['user_nickname'], username

    def request_audio_setting_handle(self, client_soc: SocketWrapper, request_data: dict):
        print('Request audio setting handle')
        username = request_data['username']
        nickname = self.clients[username]['nickname']

        # 音频用的ip和端口
        self.audio_ip = get_ip_address("WLAN")
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket.bind((self.audio_ip, AUDIO_PORT))
        self.audio_socket.listen(100)
        self.audio_clients = []
        print('Running on IP: ' + self.audio_ip)

        # 拼接返回信息
        msg = ResponseProtocol.response_audio_setting(nickname, self.audio_ip, str(AUDIO_PORT))
        for u_name, client in self.clients.items():
            client['sock'].send_data(msg)

        # 开启音频线程
        self.set_audio = True
        while self.set_audio:
            try:
                c, addr = self.audio_socket.accept()
            except:
                self.set_audio = False
                print('Close audio')
                break

            self.audio_clients.append(c)

            thread_num = Thread(target=self.audio_handle, args=(c, addr,))
            thread_num.start()
            self.thread_set.append(thread_num)

    def voice_Call_Broadcast(self, sock, data):
        for client in self.audio_clients:
            if client != self.server_socket and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def audio_handle(self, c, addr):
        while self.set_audio:
            try:
                data = c.recv(1024)
                self.voice_Call_Broadcast(c, data)
            except socket.error:
                c.close()

    def request_audio_close_handle(self, client_soc: SocketWrapper, request_data: dict):
        print('Request audio close handle')
        self.set_audio = False
        if self.audio_socket:
            self.audio_socket.close()
        print('Close audio socket')
        if self.audio_thread:
            self.audio_thread.join()
        for thread in self.thread_set:
            if thread:
                thread.join()
        self.thread_set.clear()
        self.audio_clients.clear()
        self.audio_ip = None
        self.audio_socket = None
        self.audio_thread = None
        self.set_audio = True

        username = request_data['username']
        nickname = self.clients[username]['nickname']
        print('Close audio:', nickname)
        for u_name, client in self.clients.items():
            if u_name == username:
                continue
            client['sock'].send_data(ResponseProtocol.response_audio_close(nickname))
        print('Close audio')


if __name__ == '__main__':
    server = Server()
    server.startup()
