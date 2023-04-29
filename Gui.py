from prettytable import PrettyTable

class GuiIgorBank:

    def __init__(self) -> None:
        self.table = PrettyTable(["TIME_STAMP", "TRANSMISSOR", "RECEPTOR", "VALUE", "OPERATION"])

        self.table.align["TIME_STAMP"] = "l"
        self.table.align["TRANSMISSOR"] = "l"
        self.table.align["RECEPTOR"] = "l"
        self.table.align["VALUE"] = "l"
        self.table.align["OPERATION"] = "l"

    def updateGui(self, *args):
        print("\x1b[2J")

        self.table.add_row(args)
        print(self.table)
        print("\n")