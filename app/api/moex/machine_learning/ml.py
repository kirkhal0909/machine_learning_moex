from app.api.moex.machine_learning.data_moex import DataMoex
from app.api.moex.machine_learning.model import Model
from app.api.moex.machine_learning.dataframe import Dataframe

class ML():
  def __init__(self, client, parser) -> None:
    self.data = DataMoex(client, parser)
    self.model = Model()
    self.dataframe = Dataframe()

