from threading import Thread
import socket

class Protocol:

    SEPARATOR = '|'
    REQUEST = 'REQUEST'
    GRANT = 'GRANT'
    OPERATION_SEND_PIX = 'OPERATION_CRED'
    OPERATION_RESULT = 'OPERATION_RESULT'
    RELEASE = 'RELEASE'
    MSG_SIZE = 8

    SUCESS = '00000000'
    FAILURE = '00000001'

    def __init__(self) -> None:
        self.host = '127.0.0.1'
        self.port = 55125
        self.data_size = 1024
        self.mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)