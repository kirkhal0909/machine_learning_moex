from app.api.moex.machine_learning.data_moex import DataMoex
from app.api.moex.machine_learning.data_fit import DataFit
from app.api.moex.machine_learning.model import Model
from app.api.moex.machine_learning.dataframe import Dataframe

import numpy as np

class ML():
  def __init__(self, client, parser, model_version = 1, config = {}) -> None:
    self.config = {
      'epochs': 64,
      'normalization_type': None, # or 'candles' or 'less_more'
      'lstm_range': 30,
      'model_neurons1': 64,
      'model_neurons2': None,
      'data_length': None,
      'load_model': True,
    }
    self.data = DataMoex(client, parser)
    self.data_fit = DataFit()
    self.model = Model(model_version, self.config)
    self.dataframe = Dataframe(self.data)
    self.update_configs(config)
    self.__last__ = {}

  def fit(self, ticker='ALL'):
    try:
      x, y = self.__last__[ticker]['x'], self.__last__[ticker]['y']
    except:
      x, y = self.data_fit.get_x_y(self.dataframe.get_dataframes(ticker), self.config['lstm_range'])
      self.__last__[ticker] = { 'x': x, 'y': y }
    x, y = x[:self.config['data_length']], y[:self.config['data_length']]
    model = self.model.fit(x, y, epochs=self.config['epochs'])
    return x, y, model

  def update_configs(self, config={}):
    self.config = {
      **self.config,
      **config,
    }
    self.config = {
      **self.config,
      'output_dense': 2 if self.config.get('normalization_type') != None else 1
    }
    self.model.config = self.config
    self.dataframe.config = self.config

  def predict(self, x):
    y_scalled = self.model.__model__.predict(x)
    return self.data_fit.unscale(y_scalled)
