import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

class DataFit():
  def __init__(self) -> None:
    self.__scale_range__ = (0, 1)
    self.__scaler_path__ = 'models/scaler_{}_{}.pkl'.format(self.__scale_range__[0], self.__scale_range__[1])
    self.scaler = self.load_or_create_scaler()

  def load_or_create_scaler(self):
    if os.path.exists(self.__scaler_path__):
      return joblib.load(self.__scaler_path__)
    return MinMaxScaler(feature_range=self.__scale_range__)

  def get_x_y(self, dataframes, x_range=30):
    y = []
    x = []
    for dataframe_normalized in dataframes:
      dataframe = dataframe_normalized.copy()
      y += list(dataframe.tomorrow_close[x_range - 1:])
      dataframe = dataframe.drop(columns=['tomorrow_close'])
      x += [windowed for windowed in dataframe.rolling(window=x_range)][x_range - 1:]
    y_scalled = self.scale(np.array(y).reshape(len(y), 1))
    x_scalled = np.array(x).reshape(-1, 1).reshape(len(x), len(x[0]), x[0].shape[1] )
    return x_scalled, y_scalled

  def scale(self, data_series):
    self.scaler = self.scaler.fit(data_series)
    scaled = self.scaler.transform(data_series)
    joblib.dump(self.scaler, self.__scaler_path__)

    return scaled

  def unscale(self, data_series):
    return self.scaler.inverse_transform(data_series)
