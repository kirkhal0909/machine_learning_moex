from app.api.bcs.bcs_client import BCSClient
from app.api.bcs.bcs_parser import BCSParser

class BCS():
    def __init__(self) -> None:
        self.client = BCSClient()
        self.parser = BCSParser(self.client)