from app.api.moex.moex_client import MOEXClient
from app.api.moex.moex_parser import MOEXParser

class MOEX():
  def __init__(self):
    self.client = MOEXClient()
    self.parser = MOEXParser(self.client)