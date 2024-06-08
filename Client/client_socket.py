import socket
from config import *


class ClientSocket(socket.socket):
    def __init__(self):
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        super(ClientSocket, self).connect((ip, port))

    def recv_data(self):
        return self.recv(1024).decode('utf-8')

    def send_data(self, data):
        self.send(data.encode('utf-8'))

    def recv_file(self, file_name):
        with open(file_name, 'wb') as f:
            while True:
                data = self.recv(1024)
                # print(data)
                if not data:# data == END_OF_SEND:
                    break
                f.write(data)

    def send_file(self, file_name):
        with open(file_name, 'rb') as f:
            while True:
                data = f.read(1024)
                self.send(data)
                print(185)
                if not data:
                    # self.send(END_OF_SEND)
                    break

