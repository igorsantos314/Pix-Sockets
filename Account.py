from prettytable import PrettyTable
from BaseProtocol import *
from datetime import datetime

class Account:

    def __init__(self, email, password, pix_key, initial_cash = 0) -> None:
        self.email = email
        self.password = password
        
        self.pix_key = pix_key
        self.cash = initial_cash
        self.operations = []

        self.table = PrettyTable(["OPERATION_TYPE", "UID", "VALUE", "TIME_STAMP"])

        self.table.align["OPERATION_TYPE"] = "l"
        self.table.align["UID"] = "l"
        self.table.align["VALUE"] = "l"
        self.table.align["TIME_STAMP"] = "l"

        self.table.padding_width = 1

    def debt(self, origin_key, value):
        operation_info = [
            Protocol.DEBT_VALUE_SEND_PIX,
            origin_key,
            value,
            datetime.now()
        ]

        self.cash -= value
        self.operations.append(operation_info)
        self.table.add_row(operation_info)

    def cred(self, origin_key, value):
        operation_info = [
            Protocol.CREDIT_VALUE_RECEIVE_BY_PIX,
            origin_key,
            value,
            datetime.now()
        ]

        self.cash += value
        self.operations.append(operation_info)
        self.table.add_row(operation_info)

    def view(self):
        print(f"PIX KEY={self.pix_key.upper()}")
        print(f"AVAIBLE CASH=R$ {self.cash}")
        print(self.table)
        print("\n\n")
