from threading import Thread
import socket

class Protocol:
    EMPTY = ""

    ON_HOLD = 'ON_HOLD'
    RELEASED = 'RELEASED'
    RUNNING = 'RUNNING'

    SEPARATOR = '|'
    REQUEST = 'REQUEST'
    GRANT = 'GRANT'
    OPERATION_SEND_PIX = 'OPERATION_SEND_PIX'
    OPERATION_RESULT = 'OPERATION_RESULT'
    RELEASE = 'RELEASE'
    TIME_OUT = 'TIME_OUT'
    MSG_SIZE = 8

    DEBT_VALUE_SEND_PIX = 'DEBT_VALUE_SEND_PIX'
    CREDIT_VALUE_RECEIVE_BY_PIX = 'CREDIT_VALUE_RECEIVE_BY_PIX'

    SUCESS = 'SUCCESS'
    FAILURE = 'FAILURE'

    def __init__(self) -> None:
        self.host = '127.0.0.1'
        self.port = 55125
        self.data_size = 4096
        self.mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)