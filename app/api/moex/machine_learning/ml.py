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
      'output_less_more': False,
      'data_length': None,
      'load_model': True,
    }
    self.data = DataMoex(client, parser)
    self.data_fit = DataFit()
    self.model = Model(model_version, self.config)
    self.dataframe = Dataframe(self.data)
    self.update_configs(config)

  def fit(self, ticker='ALL'):
    x, y = self.data_fit.get_x_y(self.dataframe.get_dataframes(ticker), self.config['lstm_range'])
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
      'output_dense': 2 if self.config.get('output_less_more') else 1
    }
    self.model.config = self.config
    self.dataframe.config = self.config

  def predict(self, x):
    y_scalled = self.model.model().predict(x)
    return self.data_fit.unscale(y_scalled)
