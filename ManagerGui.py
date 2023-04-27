from tkinter import *
from tkinter import ttk
from threading import Thread
from time import sleep
from prettytable import PrettyTable
import subprocess

class ManagerGui:

    def __init__(self, manager) -> None:
        self.manager = manager

        # Cria a tabela
        self.table = PrettyTable(["OPERATION", "UID", "VALUE", "RECEPTOR_PIX_KEY", "STATUS"])

        # Alinha as colunas
        self.table.align["OPERATION"] = "l"
        self.table.align["UID"] = "l"
        self.table.align["VALUE"] = "l"
        self.table.align["RECEPTOR_PIX_KEY"] = "l"
        self.table.align["STATUS"] = "r"

        self.table.padding_width = 1

        #-------------------------------------------------------
        self.options = PrettyTable(["CHOOSE_OPTION"])
        self.options.align["CHOOSE_OPTION"] = "l"

        self.options.add_row(["1 - VIEW ACCOUNTS"])
        self.options.add_row(["2 - QUEUE"])
        self.options.add_row(["3 - RESTART"])
        self.options.add_row(["4 - CLEAR SCREEN"])
        self.options.add_row(["5 - EXIT"])

        self.options.padding_width = 1    

    def viewAccounts(self):
        for account in self.manager.getAccounts():
            account.view()

    def viewQueue(self):
        for queue in self.manager.getQueue():
            print(queue)

    def build(self):
        while True:
            print(self.options)
            opc = input("OPTION -> ")

            if opc == '1':
                self.viewAccounts()
            
            if opc == '2':
                self.viewQueue()

            if opc == '3':
                self.clearScreen()
                print(".................... SERVER RESTARTED ....................")
                self.manager.restart()

            if opc == '4':
                self.clearScreen()

    def clearScreen(self):
        print("\x1b[2J")

    def notifyChanged(self):
        self.table.clear_rows()

debug = False

if __name__ == "__main__":
    if debug:
        mg = ManagerGui()
        sleep(2)
        mg.notifyChanged(
            [
                {
                    "process_id": "process_id",
                    "conn": "conn",
                    "status": "on_hold"
                }
            ]
        )
    