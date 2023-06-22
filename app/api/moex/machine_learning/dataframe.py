import math
import numpy as np
import pandas as pd
import talib

class Dataframe():
  def __init__(self, data_moex, config = {}) -> None:
    self.data_moex = data_moex
    self.traded_null_count_skip = 200
    self.config = config

  def get_dataframes(self, ticker):
    dataframes = []
    if ticker == 'ALL':
      tickers = self.data_moex.tickers_list()
    else:
      tickers = [ticker]
    for ticker in tickers:
      dataframe_ticker = self.data_moex.stocks_prices_all_period(ticker)
      nulls = (len(dataframe_ticker) - np.count_nonzero(dataframe_ticker.value_traded))
      if nulls < self.traded_null_count_skip:
        dataframe_normalized = self.normalize(dataframe_ticker)
        dataframes.append(dataframe_normalized)
    return dataframes

  def normalize(self, dataframe):
    dataframe = self.remove_index_and_data(dataframe)
    dataframe = self.remove_top_nan(dataframe)
    dataframe = self.classify_prices(dataframe)
    if self.config.get('normalization_type') == 'candles':
      dataframe = self.select_columns(dataframe, ['open', 'close', 'high', 'low'])
      dataframe = self.classify_candle(dataframe)
      dataframe = self.add_tomorrow_close(dataframe)
      dataframe = self.select_columns(dataframe, ['candle_classifier', 'tomorrow_close'])
      dataframe = self.output_less_more(dataframe)
    else:
      dataframe = self.classify_volumes(dataframe)
      dataframe = self.add_tomorrow_close(dataframe)
    return dataframe[1:-1].dropna()

  def remove_index_and_data(self, dataframe):
    return dataframe.copy().iloc[: , 2:]

  def remove_top_nan(self, dataframe):
    nulls = list(dataframe.imoex_low.isnull())[:-1][::-1]
    if True not in nulls:
      return dataframe
    without_top = dataframe.copy()[len(dataframe) - nulls.index(True) - 1:]
    return without_top

  def select_columns(self, dataframe, columns=[]):
    return dataframe.copy()[columns]

  def output_less_more(self, dataframe):
    dataframe = dataframe.copy()
    dataframe.tomorrow_close = dataframe.tomorrow_close.fillna(0.0).apply(np.int64)
    dataframe.tomorrow_close[dataframe.tomorrow_close < dataframe.close] = 0
    dataframe.tomorrow_close[dataframe.tomorrow_close >= dataframe.close] = 1
    return dataframe

  def classify_candle(self, dataframe):
    dataframe = dataframe.copy()
    dataframe_candles = pd.DataFrame()
    candles = talib.get_function_groups()['Pattern Recognition']
    candles_hash = { candle: candles.index(candle) * 2 for candle in candles }
    for candle in candles:
      dataframe_candles[candle] = getattr(talib, candle)(open=dataframe.open, high=dataframe.high, low=dataframe.low, close=dataframe.close)
    dataframe_candles = dataframe_candles
    dataframe_candles_transparent = dataframe_candles.T
    founded_candles = dataframe_candles_transparent[dataframe_candles_transparent != 0].idxmax()
    dataframe['candle_classifier'] = 0
    for pos in range(founded_candles.index.start, founded_candles.index.stop, 1):
      candle = founded_candles[pos]
      if candle.__class__ == str:
        if dataframe_candles[candle][pos] < 0:
          dataframe['candle_classifier'][pos] = candles_hash[candle] + 1
        else:
          dataframe['candle_classifier'][pos] = candles_hash[candle] + 2
    return dataframe

  def add_tomorrow_close(self, dataframe):
    dataframe = dataframe.copy()
    dataframe['tomorrow_close'] = dataframe.close.shift(-1)
    return dataframe

  def classify_prices(self, dataframe):
    dataframe = dataframe.copy()
    for column in dataframe.columns:
      if 'close' in column and column != 'tomorrow_close':
        interpolate_column = column.replace('close', '{}')
        col_open = list(dataframe[interpolate_column.format('open')])
        col_low = list(dataframe[interpolate_column.format('low')])
        col_high = list(dataframe[interpolate_column.format('high')])
        col_close = list(dataframe[column])
        for pos in range(len(dataframe) - 1, 0, -1):
          col_open[pos] = self.normalize_percent(col_close[pos], col_open[pos])
          col_low[pos] = self.normalize_percent(col_close[pos], col_low[pos])
          col_high[pos] = self.normalize_percent(col_close[pos], col_high[pos])
          col_close[pos] = self.normalize_percent(col_close[pos], col_close[pos - 1])
        dataframe[interpolate_column.format('open')] = np.array(col_open)
        dataframe[interpolate_column.format('low')] = np.array(col_low)
        dataframe[interpolate_column.format('high')] = np.array(col_high)
        dataframe[column] = np.array(col_close)
    return dataframe

  def classify_volumes(self, dataframe):
    dataframe = dataframe.copy()
    for column in dataframe.columns:
      if any(substring in column for substring in ['volume', 'value', 'capitalization']):
        values = [ int(value) if not math.isnan(value) else value for value in list(dataframe[column])]
        dataframe["{}_e".format(column)] = np.array([ len(str(value)) - 1 for value in values])
        rounded_prefixes = [ round(int(str(int(value)).ljust(3, '0')[:3]) / 100) if not math.isnan(value) else value for value in list(dataframe[column])]
        dataframe[column] = np.array(rounded_prefixes)
    return dataframe

  def normalize_percent(self, value1, value2, step = 0.2):
    if math.isnan(value1):
      return value1
    percent = (value1 / value2 - 1) * 100
    return int(percent // step + (percent % step * 2 // step))
