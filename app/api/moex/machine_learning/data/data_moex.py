from app.helpers.dates import minus_today
import pandas as pd
import os
from app.api.banks.ru_cb.bank_cb import BankСb
from app.api.banks.usa_federal_reserve.newyorkfred_api import NewyorkfredAPI
from curl_cffi.requests.errors import RequestsError

class DataMoex():
  def __init__(self, client, parser) -> None:
    self.client = client
    self.parser = parser
    self.__DATA_FOLDER__ = '_tickers_history'
    self.banks = [BankСb(), NewyorkfredAPI()]

  def save_all_prices(self):
    tickers = self.tickers_list()
    for ticker in tickers:
      downloaded = False
      while not downloaded:
        try:
          print("tickers {}/{}".format(tickers.index(ticker)+1, len(tickers)))
          self.stocks_prices_all_period(ticker)
          downloaded = True
        except RequestsError:
          None

  def tickers_list(self):
    return list(self.parser.today_prices().keys())[1:]

  def stocks_prices_all_period(self, ticker, load_from_file = True):
    file_path = "{}/{}.csv".format(self.__DATA_FOLDER__, ticker)
    if load_from_file and os.path.exists(file_path):
      dataframe = pd.read_csv(file_path)
    else:
      data_by_dates = {}
      days = 0
      get_date = lambda prices_row: prices_row.get('@TRADEDATE') or prices_row.get('@SYSTIME').split(' ')[0]
      get_index = lambda index, days: self.get_data(self.client.index_prices(index, { 'from': minus_today(days) }), 0)
      prices = [row for row in self.get_data(self.client.stocks_prices_today(), 1) if row['@SECID'] == ticker]

      last_date = None
      while last_date != get_date(prices[0]):
        last_date = get_date(prices[0])
        imoex = get_index('IMOEX', days)
        if days == 0:
          minus_day = 1
          while imoex == None:
            imoex = get_index('IMOEX', minus_day)
            minus_day += 1
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

      dataframe = pd.json_normalize([{ 'date': key, **data_by_dates[key] } for key in sorted(data_by_dates.keys())])
      dataframe.to_csv(file_path)
    return dataframe

  def get_data(self, response, data_position = 0):
    try:
      return response['document']['data']['rows']['row']
    except:
      if response['document']['data'][data_position]['rows'] == None:
        return None
      return response['document']['data'][data_position]['rows']['row']
