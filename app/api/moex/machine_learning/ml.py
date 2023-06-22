from app.api.moex.machine_learning.data_moex import DataMoex
from app.api.moex.machine_learning.data_fit import DataFit
from app.api.moex.machine_learning.model import Model
from app.api.moex.machine_learning.dataframe import Dataframe

import pickle

class ML():
  __FILE_CACHE__ = 'cache/ML_x_y.pickle'

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
      'batch_size': 64
    }
    self.data = DataMoex(client, parser)
    self.data_fit = DataFit()
    self.model = Model(model_version, self.config)
    self.dataframe = Dataframe(self.data)
    self.update_configs(config)
    self.__last__ = {}

  def fit(self, ticker='ALL'):
    x, y = self.data_fit.get_x_y(self.read_dataframes(ticker))
    x, y = x[:self.config['data_length']], y[:self.config['data_length']]
    model = self.model.fit(x, y, epochs=self.config['epochs'], rewrite_model = True)
    return x, y, model

  def read_dataframes(self, ticker):
    try:
      return self.read_cache(ticker)
    except:
      dataframes = self.dataframe.get_dataframes(ticker)
      self.write_cache(ticker, dataframes)
    return dataframes

  def read_cache(self, ticker = None):
    with open(self.__FILE_CACHE__, 'rb') as handle:
      try:
        data = pickle.load(handle)
        if ticker == None:
          return data
        else:
          return data[ticker]
      except:
        return {}

  def write_cache(self, ticker, dataframes):
    with open(self.__FILE_CACHE__, 'wb') as handle:
      data = self.read_cache()
      data[ticker] = dataframes
      pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

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

  def predict(self, x):
    y_scalled = self.model.__model__.predict(x)
    return self.data_fit.unscale(y_scalled)
