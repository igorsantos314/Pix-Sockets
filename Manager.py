from BaseProtocol import *
import logging
from time import sleep
from ManagerGui import ManagerGui
from datetime import datetime
from Account import Account

class AccountRepositoryMock:
    
    def __init__(self) -> None:
        self.accounts = [
            Account("igor_abc", 10),
            Account("juares_egf", 5),
            Account("veto_2asd", 78),
            Account("gabras_8s4d", 213),
            Account("matas_abc", 9),
            Account("kaique_abc", 15),
            Account("hitalo_valvo_asdasjh", 25),
        ]

    def findAccount(self, pix_key):
        for i in self.accounts:
            if i.pix_key == pix_key:
                return i

        return None
    
    def isPixPossible(self, transmitter_key, receptor_key, transfer_value):
        
        transmitter_account = self.findAccount(transmitter_key)
        receptor_account = self.findAccount(receptor_key)
        
        if transmitter_account == None or receptor_account == None:
            return None, None
        
        if transmitter_account.cash < transfer_value or transfer_value <= 0:
            return None, None
        
        return transmitter_account, receptor_account

    def sendPix(self, transmitter_key, receptor_key, transfer_value):
        transmitter_account, receptor_account = self.isPixPossible(transmitter_key, receptor_key, transfer_value)

        if type(transmitter_account) == Account:
            transmitter_account.debt(receptor_key, transfer_value)
            receptor_account.cred(transmitter_key, transfer_value)
            print("SUCESS")
            return Protocol.SUCESS
        
        print("FAILURE")
        return Protocol.FAILURE
    
class Manager(Protocol):

    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(filename="log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

        self.isNotify = False
        self.igor_bank = AccountRepositoryMock()
        self.gui = ManagerGui(self)
        self.queue = []
        self.mSocket.bind((self.host, self.port))

        self.indicator = 0

        Thread(target=self.gui.build, args=()).start()

        self.listenConnections()

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
                data = conn.recv(self.data_size).decode()
                data_list = data.split(Protocol.SEPARATOR)
            
                self.manageQueue(data_list[0], data_list[1], data_list[2], data_list[3], conn)
            except:
                pass

    def sendMessage(self, conn, msg):
        conn.sendall(str(msg).encode())
        
    def manageQueue(self, type_process_request, transfer_key, pix_key, msg, conn):
        logging.info(f"TYPE={type_process_request} PROCESS_ID={transfer_key} PIX_KEY={pix_key} MSG={msg}")

        if type_process_request == Protocol.REQUEST:
            self.queue.append(
                {
                    "process_id": transfer_key,
                    "pix_key": pix_key,
                    "conn": conn,
                    "ts": datetime.now(),
                    "status": "on_hold"
                }
            )
            if self.verifyProcessRunning() == False:
                self.grantProcessAccess()

        elif type_process_request == Protocol.RELEASE:
            #conn.close()
            self.queue[self.indicator]["status"] = "released"
            self.indicator += 1
            
            if self.indicator < len(self.queue):
                self.grantProcessAccess()

        elif type_process_request == Protocol.OPERATION_SEND_PIX:
            result = self.igor_bank.sendPix(transfer_key, pix_key, int(msg))
            print(result)

            self.sendMessage(
                self.queue[self.indicator]["conn"],
                f"{Protocol.OPERATION_RESULT}{Protocol.SEPARATOR}{transfer_key}{Protocol.SEPARATOR}{result}"
            )
            
    def verifyProcessRunning(self) -> bool:
        process = self.queue[-1]
        return process["status"] == "running"

    def grantProcessAccess(self):
        current_process = self.queue[self.indicator]
        process_id = current_process['process_id']
        self.queue[self.indicator]["status"] = "running"

        self.sendMessage(
            current_process["conn"],
            f"{Protocol.GRANT}{Protocol.SEPARATOR}process_id={process_id}{Protocol.SEPARATOR}00000000"
        )
        
        #logging.info(f"TYPE={Protocol.GRANT} PROCESS_ID={process_id} MSG=00000000")

if __name__ == "__main__":
    Manager()