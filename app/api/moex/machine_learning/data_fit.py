import numpy as np

class DataFit():
  def get_x_y(self, dataframes, x_range=30):
    y = []
    x = []
    for dataframe_normalized in dataframes:
      dataframe = dataframe_normalized.copy()
      y += list(dataframe.tomorrow_close[x_range - 1:])
      dataframe = dataframe.drop(columns=['tomorrow_close'])
      x += [windowed for windowed in dataframe.rolling(window=x_range)][x_range - 1:]
    return np.array(x), np.array(y)
