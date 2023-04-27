from BaseProtocol import *
from datetime import datetime
from time import sleep
from random import randint

class Process(Protocol):

    def __init__(self, uid, time_sleep, receptors_pix, value) -> None:
        super().__init__()
        
        self.current_number_operation = 0

        self.time_sleep = time_sleep
        self.uid = uid
        self.receptors_pix = receptors_pix
        self.value = value

        self.mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mSocket.connect((self.host, self.port))

        Thread(target=self.requestOperation).start()
        Thread(target=self.listen).start()

    def listen(self):
        while True:
            data = self.mSocket.recv(self.data_size).decode()
            data_list = data.split(Protocol.SEPARATOR)

            print(data)

            if data_list[0] == Protocol.GRANT:
                self.operation(
                    self.receptors_pix[self.current_number_operation],
                    self.value
                )

            elif data_list[0] == Protocol.OPERATION_RESULT:
                if data_list[2] == Protocol.SUCESS:
                    self.current_number_operation += 1
                    self.requestOperation()

    def operation(self, pix_key, value):
        print("Operation granted")

        self.send(
            Protocol.OPERATION_SEND_PIX,
            self.getValueFormated(value),
            pix_key
        )

        sleep(self.time_sleep)
        
        self.send(Protocol.RELEASE)
    
    def requestOperation(self):
        if self.current_number_operation < len(self.receptors_pix):
            self.send(
                Protocol.REQUEST
            )

    def getTimeStampFormatted(self) -> str:
        time_stamp = datetime.now().strftime("%H:%M:%S")
        return f"PROCESS_ID={self.uid} TIME_STAMP={time_stamp}\n" 

    def send(self, type_protocol, msg = "00000000", pix_key = "0"):
        data_send_formatted = f"{type_protocol}{Protocol.SEPARATOR}{self.uid}{Protocol.SEPARATOR}{pix_key}{Protocol.SEPARATOR}{msg}"
        self.mSocket.sendall(data_send_formatted.encode())

    def getValueFormated(self, value):
        len_value = len(str(value))
        value_f = f"{(Protocol.MSG_SIZE - len_value) * '0'}{value}"

        return value_f
    
Process("gabras_8s4d", 2, ["igor_abc", "veto_2asd"], 3)