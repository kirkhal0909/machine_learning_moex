from app.helpers.dates import minus_today
from app.api.banks.ru_cb.bank_cb import BankСb
from app.api.banks.usa_federal_reserve.newyorkfred_api import NewyorkfredAPI
import pandas as pd

class MOEXTensorflowData():
  def __init__(self, client, input_length = 7):
    self.client = client
    self.banks = [BankСb(), NewyorkfredAPI()]
    self.input_length = input_length

  def get_data(self, response, data_position = 0):
    try:
      return response['document']['data']['rows']['row']
    except:
      if response['document']['data'][data_position]['rows'] == None:
        return None
      return response['document']['data'][data_position]['rows']['row']

  def get_x_y(self, ticker):
    dataframe = self.prepare_dataframe(ticker)
    X = []
    Y = dataframe.close.shift(-1).dropna()[self.input_length - 1:].values

    normalized_dataframe = self.normalize_dataframe(dataframe)

    for pos in range(self.input_length, len(normalized_dataframe), 1):
      X.append(normalized_dataframe[pos - self.input_length: pos])

    last_sequence = normalized_dataframe[-self.input_length:]

    return X, Y, last_sequence, normalized_dataframe

  def prepare_dataframe(self, ticker, days_mean=30):
    data_by_dates = self.stocks_prices_all_period(ticker)
    dataframe = pd.json_normalize([data_by_dates[key] for key in sorted(data_by_dates.keys())]).dropna()
    dataframe['close_avg_30'] = dataframe.close.ewm(com = days_mean, adjust = False).mean(numeric_only=True)
    dataframe['imoex_close_avg_30'] = dataframe.imoex_close.ewm(com = days_mean, adjust = False).mean(numeric_only=True)
    return dataframe[days_mean:]

  def normalize_dataframe(self, dataframe, round_value = 4):
    return round((dataframe - dataframe.min()) / (dataframe.max() - dataframe.min()), round_value)

  def stocks_prices_all_period(self, ticker):
    data_by_dates = {}
    days = 0
    get_date = lambda prices_row: prices_row.get('@TRADEDATE') or prices_row.get('@SYSTIME').split(' ')[0]
    get_index = lambda index, days: self.get_data(self.client.index_prices(index, { 'from': minus_today(days) }), 0)
    prices = [row for row in self.get_data(self.client.stocks_prices_today(), 1) if row['@SECID'] == ticker]

    while not data_by_dates.get(get_date(prices[0])):
      imoex = get_index('IMOEX', days)
      if days == 0 and imoex == None:
        imoex = get_index('IMOEX', 1)
      for row in prices:
        if row['@OPEN']:
          date = get_date(row)
          data_by_dates[date] = {
            'open': float(row['@OPEN']),
            'close': float(row.get('@CLOSE') or row.get('@MARKETPRICE')),
            'high': float(row['@HIGH']),
            'low': float(row['@LOW']),
            'volume': float(row.get('@VOLUME') or row['@VOLTODAY']),
            'value_traded': float(row.get('@MP2VALTRD') or row['@VALTODAY']),
          }
          for bank in self.banks:
            try:
              data_by_dates[date]["key_rate_{}".format(bank.__class__.__name__)] = bank.key_rate_by(date)
            except:
              print('Some error with key rate bank {}'.format(bank.__class__.__name__))
      for row in [imoex] if imoex.__class__ == dict else imoex:
        if data_by_dates.get(get_date(row), {}):
          data_by_dates[get_date(row)] = {
            **data_by_dates.get(get_date(row)),
            'imoex_open': float(row.get('@OPEN')),
            'imoex_close': float(row.get('@CLOSE')),
            'imoex_high': float(row.get('@HIGH')),
            'imoex_low': float(row.get('@LOW')),
            'imoex_value': float(row.get('@VALUE')),
            'imoex_capitalization': float(row.get('@CAPITALIZATION'))
          }
      days += 90
      prices = self.get_data(self.client.stock_prices(ticker, { 'from': minus_today(days) }), 1)

    return data_by_dates
