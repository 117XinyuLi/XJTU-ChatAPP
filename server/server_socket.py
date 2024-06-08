import socket
from config import *


class ServerSocket(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
        self.bind((SERVER_IP, SERVER_PORT))  # Bind the socket to the address and port
        self.listen(128)  # Enable the server to accept connections

