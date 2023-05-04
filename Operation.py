from BaseProtocol import Protocol
from Transfer import Transfer

class Operation:

    def __init__(self, operation = Protocol.EMPTY, transfer: Transfer = None, conn = None) -> None:
        self.operation = operation
        self.transfer = transfer
        self.conn = conn
        self.status = Protocol.ON_HOLD

    def __str__(self) -> str:
        return f"OPERATION - operation={self.operation}, transfer=({self.transfer})"