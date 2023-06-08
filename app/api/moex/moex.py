from app.api.moex.moex_client import MOEXClient
from app.api.moex.moex_parser import MOEXParser
from app.api.moex.moex_tensorflow_data import MOEXTensorflowData

class MOEX():
  def __init__(self):
    self.client = MOEXClient()
    self.parser = MOEXParser(self.client)
    self.tensorflow_data = MOEXTensorflowData(self.client)
