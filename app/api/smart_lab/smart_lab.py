from app.api.smart_lab.smart_lab_client import SmartLabClient
from app.api.smart_lab.smart_lab_parser import SmartLabParser

class SmartLab():
  def __init__(self) -> None:
    self.client = SmartLabClient()
    self.parser = SmartLabParser(self.client)
