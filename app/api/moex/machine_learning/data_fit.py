import numpy as np

class DataFit():
  def get_x_y(dataframe, x_range=30):
    dataframe = dataframe.copy()
    y = np.array(dataframe.tomorrow_close[x_range - 1:])
    dataframe = dataframe.drop(columns=['tomorrow_close'])
    x = np.array([windowed for windowed in dataframe.rolling(window=x_range)][x_range - 1:])
    return x, y
