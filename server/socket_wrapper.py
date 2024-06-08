from config import *


class SocketWrapper(object):
    def __init__(self, socket):
        self.socket = socket

    def send_data(self, message):
        return self.socket.send(message.encode('utf-8'))

    def recv_data(self):
        try:
            return self.socket.recv(1024).decode('utf-8')
        except:
            return ""

    def send_file(self, file):
        with open(file, 'rb') as f:
            while True:
                data = f.read(1024)
                self.socket.send(data)
                if not data:
                    # 发送EOF
                    self.socket.send(END_OF_SEND)
                    break

        return True

    def recv_file(self, file):
        with open(file, 'wb') as f:
            while True:
                data = self.socket.recv(1024)
                if data == END_OF_SEND:
                    break
                f.write(data)

        return True

    def close(self):
        self.socket.close()
