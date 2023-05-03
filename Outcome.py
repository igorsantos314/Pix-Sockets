from BaseProtocol import Protocol

class Outcome:
    def __init__(self, response = Protocol.EMPTY, status = Protocol.EMPTY, debug_message = "") -> None:
        self.status = status
        self.response = response
        self.debug_message = debug_message

    def __str__(self) -> str:
        return f"OUTCOME - status={self.status}, response={self.response}, debug_message={self.debug_message}"