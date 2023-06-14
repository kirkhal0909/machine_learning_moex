from app.api.moex.machine_learning.data_moex import DataMoex
from app.api.moex.machine_learning.data_fit import DataFit
from app.api.moex.machine_learning.model import Model
from app.api.moex.machine_learning.dataframe import Dataframe

class ML():
  def __init__(self, client, parser) -> None:
    self.data = DataMoex(client, parser)
    self.data_fit = DataFit()
    self.model = Model()
    self.dataframe = Dataframe()

  def fit(self, ticker):
    dataframe_ticker = self.data.stocks_prices_all_period(ticker)
    dataframe_normalized = self.dataframe.normalize(dataframe_ticker)
    x, y = self.data_fit.get_x_y(dataframe_normalized)
    model = self.model.fit(x, y)
    return x, y, model
