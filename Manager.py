from BaseProtocol import *
import logging
from time import sleep
from ManagerGui import ManagerGui
from datetime import datetime
from Account import Account
from Operation import Operation
from Outcome import Outcome
from Transfer import Transfer
from User import User

import pickle

class AccountRepositoryMock:
    
    def __init__(self) -> None:
        self.accounts = [
            Account("a", "b", "igor_abc", 1500),
            Account("a", "b", "juares_egf", 1500),
            Account("a", "b", "veto_2asd", 1500),
            Account("a", "b", "gabras_8s4d", 1500),
            Account("a", "b", "matas_abc", 1500),
            Account("a", "b", "kaique_abc", 1500),
            Account("a", "b", "hitalo_calvo_asdasjh", 1500),
        ]

    def findAccount(self, pix_key):
        for i in self.accounts:
            if i.pix_key == pix_key:
                return i

        return None

    def userAuthenticated(self, user: User) -> bool:
        account = self.findAccount(user.pix_key)

        if account == None:
            return False
        
        elif account.email == user.email and account.password == user.password:
            return True
        
        return False

    def isPixPossible(self, user: User, receptor_key, transfer_value):
        if self.userAuthenticated(user) == False:
            print("Auth Failure")
            return None, None

        transmitter_account = self.findAccount(user.pix_key)
        receptor_account = self.findAccount(receptor_key)

        if transmitter_account == receptor_account:
            return None, None

        if transmitter_account == None or receptor_account == None:
            return None, None
        
        if transmitter_account.cash < transfer_value or transfer_value <= 0:
            return None, None
        
        return transmitter_account, receptor_account

    def sendPix(self, transfer: Transfer):
        transmitter_account, receptor_account = self.isPixPossible(
            transfer.user_credentials, 
            transfer.receptor, 
            transfer.value
        )

        if type(transmitter_account) == Account:
            transmitter_account.debt(transfer.receptor, transfer.value)
            receptor_account.cred(transfer.user_credentials.pix_key, transfer.value)

            return Protocol.SUCCESS
        
        return Protocol.FAILURE
    
class Manager(Protocol):

    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(filename="log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

        self.time_out_started = False
        self.running = True
        self.last_time_stamp = 0

        self.isNotify = False
        self.igor_bank = AccountRepositoryMock()
        self.gui = ManagerGui(self)
        self.queue = []
        self.mSocket.bind((self.host, self.port))

        self.indicator = 0

        Thread(target=self.gui.build, args=()).start()

        self.listenConnections()

    def updateTimeStamp(self):
        self.running = True
        self.last_time_stamp = datetime.now().timestamp()

    def restart(self):
        self.queue.clear()

    def getQueue(self):
        return self.queue
    
    def getAccounts(self):
        return self.igor_bank.accounts

    def listenConnections(self):
        while True:
            self.mSocket.listen()
            Thread(target=self.acceptConnectionThread, args=()).start()
    
    def acceptConnectionThread(self):
        conn, addr = self.mSocket.accept()

        while True:
            try:
                data = conn.recv(self.data_size)
                data_operation = pickle.loads(data)
                data_operation.conn = conn

                self.manageQueue(data_operation)
            except:
                pass
        
    def manageQueue(self, operation: Operation):
        logging.debug(f"{operation}")

        if operation.operation == Protocol.REQUEST:
            self.queue.append(operation)

            if self.verifyProcessRunning() == False:
                self.grantProcessAccess()

        elif operation.operation == Protocol.RELEASE:
            self.queue[self.indicator].status = Protocol.RELEASED
            self.indicator += 1
            
            if self.indicator < len(self.queue):
                self.grantProcessAccess()

        elif operation.operation == Protocol.OPERATION_SEND_PIX:
            result = self.igor_bank.sendPix(operation.transfer)

            print(result)

            self.queue[self.indicator].conn.sendall(pickle.dumps(
                Outcome(Protocol.OPERATION_RESULT, result)
            ))
            
    def verifyProcessRunning(self) -> bool:
        return self.queue[-1].status == Protocol.RUNNING

    def grantProcessAccess(self):
        self.queue[self.indicator].status = Protocol.RUNNING

        self.queue[self.indicator].conn.sendall(pickle.dumps(
            Outcome(Protocol.GRANT)
        ))
        
if __name__ == "__main__":
    Manager()