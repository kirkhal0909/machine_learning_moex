import os
import pickle

class DataCache():
  __FILE_CACHE__ = 'cache/ML_data_cache.pickle'
  __INCLUDE_KEYS__ = ['model_type', 'normalization_type', 'input_range', 'data_length']

  def __init__(self) -> None:
    self.config = {}
    self.data_cache = self.read()

  def read(self, ticker = None, data_type = 'dataframe'):
    if os.path.exists(self.__FILE_CACHE__):
      with open(self.__FILE_CACHE__, 'rb') as handle:
        self.data_cache = pickle.load(handle)
        if ticker == None:
          return self.data_cache
        else:
          return self.get(ticker, data_type)
    else:
      return {}

  def get(self, ticker, data_type = 'dataframe'):
    if self.config.get('x_y_cache'):
      return self.data_cache.get(self.key(ticker, data_type))

  def write(self, data, ticker, data_type = 'dataframe'):
    with open(self.__FILE_CACHE__, 'wb') as handle:
      self.data_cache[self.key(ticker, data_type)] = data
      pickle.dump(self.data_cache, handle, protocol=pickle.HIGHEST_PROTOCOL)

  def key(self, ticker, data_type):
    if data_type == 'dataframe':
      return "{}_dataframe".format(ticker)
    config_block = { key:self.config[key] for key in self.__INCLUDE_KEYS__ }
    return "{}_{}_{}".format(data_type, ticker, str(config_block))
