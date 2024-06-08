import socket
from config import *
import threading
import pyaudio

is_audio = True


def receive_server_data(s, playing_stream):
    global is_audio
    while is_audio:
        try:
            data = s.recv(1024)
            playing_stream.write(data)
        except:
            pass


def send_data_to_server(s, recording_stream):
    global is_audio
    while is_audio:
        try:
            data = recording_stream.read(1024)
            s.sendall(data)
        except:
            pass


def test():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8090))

    while True:
        msg = input('Please input message: ')
        client.send(msg.encode('utf-8'))

        data = ''
        if msg.split(DELIMITER)[0] != '0005':
            data = client.recv(1024).decode('utf-8')
            print('Received:', data)

        # 开启语音
        if data.split(DELIMITER)[0] == '1004':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_ip = data.split(DELIMITER)[2]
            target_port = int(data.split(DELIMITER)[3])
            s.connect((target_ip, target_port))
            print('Connected to Audio Server')
            chunk_size = 1024  # 512
            audio_format = pyaudio.paInt16
            channels = 1
            rate = 20000
            p = pyaudio.PyAudio()
            playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                         frames_per_buffer=chunk_size)
            recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                           frames_per_buffer=chunk_size)

            receive_thread = threading.Thread(target=receive_server_data, args=(s, playing_stream,))
            receive_thread.start()
            send_thread = threading.Thread(target=send_data_to_server, args=(s, recording_stream,))
            send_thread.start()
            print('Connected to Server')

        # 关闭语音
        if msg.split(DELIMITER)[0] == '0005' or data.split(DELIMITER)[0] == '1005':
            global is_audio
            is_audio = False
            if s:
                s.close()
                s = None
            if p:
                p.terminate()
                p = None
            if playing_stream:
                playing_stream.close()
                playing_stream = None
            if recording_stream:
                recording_stream.close()
                recording_stream = None
            if send_thread:
                send_thread.join()
                send_thread = None
            if receive_thread:
                receive_thread.join()
                receive_thread = None
            is_audio = True
            print('Close audio')

    client.close()


if __name__ == '__main__':
    test()
