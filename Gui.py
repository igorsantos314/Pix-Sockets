from prettytable import PrettyTable
from Transfer import Transfer

class GuiIgorBank:

    def __init__(self) -> None:
        self.table = PrettyTable(["TIME_STAMP", "TRANSMISSOR", "RECEPTOR", "VALUE", "OPERATION"])

        self.table.align["TIME_STAMP"] = "l"
        self.table.align["TRANSMISSOR"] = "l"
        self.table.align["RECEPTOR"] = "l"
        self.table.align["VALUE"] = "l"
        self.table.align["OPERATION"] = "l"

    def updateGui(self, time_stamp, transfer: Transfer, type, show = False):
        #print("\x1b[2J")

        self.table.add_row(
            [
                time_stamp,
                transfer.user_credentials.pix_key,
                transfer.receptor,
                transfer.value,
                type
            ]
        )

        if show:
            print(self.table)
            print("\n")