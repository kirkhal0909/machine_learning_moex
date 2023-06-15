from app.api.moex.machine_learning.data_moex import DataMoex
from app.api.moex.machine_learning.data_fit import DataFit
from app.api.moex.machine_learning.model import Model
from app.api.moex.machine_learning.dataframe import Dataframe

class ML():
  def __init__(self, client, parser, model_version = 1) -> None:
    self.data = DataMoex(client, parser)
    self.data_fit = DataFit()
    self.model = Model(model_version)
    self.dataframe = Dataframe(self.data)

  def fit(self, ticker='ALL'):
    x, y = self.data_fit.get_x_y(self.dataframe.get_dataframes(ticker))
    y_scaled = self.data_fit.scale(y)
    model = self.model.fit(x, y_scaled)
    return x, y, model
