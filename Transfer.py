from User import User
from BaseProtocol import Protocol

class Transfer:
    def __init__(self, user_credentials: User, receptor, value) -> None:
        self.type = Protocol.EMPTY
        self.user_credentials = user_credentials
        self.receptor = receptor
        self.value = value

        self.status = Protocol.EMPTY

    def __str__(self) -> str:
        return f"TRANSFER - type={self.type}, user_credentials=({self.user_credentials}), receptor={self.receptor}, value={self.value}, status={self.status}"
