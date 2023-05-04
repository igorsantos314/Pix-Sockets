from BaseProtocol import *
from datetime import datetime
from time import sleep
from random import randint
from Gui import GuiIgorBank
from User import User
from Transfer import Transfer
from Operation import Operation
import pickle

class Process(Protocol):

    def __init__(self, tranfers, time_sleep) -> None:
        super().__init__()
        
        self.tranfers = tranfers
        self.current_number_operation = 0

        self.time_sleep = time_sleep
        self.bank_gui = GuiIgorBank()
        
        self.mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mSocket.connect((self.host, self.port))

        Thread(target=self.requestOperation).start()
        Thread(target=self.listen).start()

    def listen(self):
        while True:
            data = self.mSocket.recv(self.data_size)
            outcome = pickle.loads(data)

            if outcome.response == Protocol.GRANT:
                self.updateUI("SERVER_REQUEST_GRANTED")
                self.operation(
                    self.tranfers[self.current_number_operation]
                )

            elif outcome.response == Protocol.OPERATION_RESULT:
                if outcome.status == Protocol.SUCCESS:
                    self.updateUI("OPERATION_RESULT_SUCESS", True)

                    self.current_number_operation += 1
                    self.requestOperation()
                else:
                    self.updateUI("OPERATION_RESULT_FAILURE", True)

    def operation(self, transfer):
        self.updateUI(Protocol.OPERATION_SEND_PIX)
        transfer.type = Protocol.OPERATION_SEND_PIX

        self.mSocket.sendall(pickle.dumps(Operation(Protocol.OPERATION_SEND_PIX, transfer)))

        sleep(self.time_sleep)
        
        self.mSocket.sendall(pickle.dumps(Operation(Protocol.RELEASE)))

    def requestOperation(self):
        if self.current_number_operation < len(self.tranfers):
            self.updateUI(Protocol.REQUEST)
            self.mSocket.sendall(pickle.dumps(Operation(Protocol.REQUEST)))

    def updateUI(self, protocol_type, show = False):
        self.bank_gui.updateGui(datetime.now(), self.tranfers[self.current_number_operation], protocol_type, show)
    
"""user = User("a", "basd", "gabras_8s4d")

Process(
    [
        Transfer(user, "igor_abc", 3),
        Transfer(user, "veto_2asd", 3)
    ],
    time_sleep=2
)"""