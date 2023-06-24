from app.api.moex.machine_learning.data.data_cache import DataCache
from app.api.moex.machine_learning.data.data_moex import DataMoex
from app.api.moex.machine_learning.data.data_fit import DataFit
from app.api.moex.machine_learning.model import Model
from app.api.moex.machine_learning.dataframe import Dataframe

import pickle

class ML():
  def __init__(self, client, parser, model_version = 1, config = {}) -> None:
    self.config = {
      'model_type': 'LSTM',
      'epochs': 64,
      'normalization_type': None, # or 'candles' or 'less_more'
      'input_range': 30,
      'model_neurons1': 64,
      'model_neurons2': None,
      'data_length': None,
      'load_model': True,
      'batch_size': 64,
      'x_y_cache': False
    }
    self.cache = DataCache()
    self.data = DataMoex(client, parser)
    self.data_fit = DataFit()
    self.model = Model(model_version, self.config)
    self.dataframe = Dataframe(self.data)
    self.update_configs(config)
    self.__last__ = {}

  def fit(self, ticker='ALL', rewrite_model = True):
    x, y, last_sequences = self.read_x_y_last_seq(ticker)
    model = self.model.fit(x, y, epochs=self.config['epochs'], rewrite_model = rewrite_model)
    return x, y, last_sequences, model

  def read_x_y_last_seq(self, ticker):
    x, y, last_sequence = self.cache.get(ticker, 'x__y__last_sequence') or [None, None, None]
    if x is None or y is None:
      x, y, last_sequences = self.data_fit.get_x_y_last_seq(self.read_dataframes(ticker))
      x, y = x[:self.config['data_length']], y[:self.config['data_length']]
      self.cache.write([x, y, last_sequence], ticker, 'x__y__last_sequence')
    return x, y, last_sequences

  def read_dataframes(self, ticker):
    dataframes = self.cache.get(ticker)
    if dataframes is None:
      dataframes = self.dataframe.get_dataframes(ticker)
      self.cache.write(dataframes, ticker)
    return dataframes

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
    self.data_fit.config = self.config
    self.cache.config = self.config

  def predict(self, x):
    y_scalled = self.model.__model__.predict(x)
    return self.data_fit.unscale(y_scalled)
