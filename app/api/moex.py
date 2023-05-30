from curl_cffi import requests
import xmltodict
import json
import urllib

import pickle

from app.helpers.dates import minus_today

class MOEX():
  def __init__(self):
    self.client = self.Client()
    self.parser = self.Parser(self.client)

  class Client():
    STOCKS_LIST_URL = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities'
    INDEXES_LIST_URL = 'https://iss.moex.com/iss/history/engines/stock/markets/index/securities'
    TICKERS_BY_INDEX = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/{}/tickers'
    MOEX_NEWS_LINK = 'https://iss.moex.com/iss/sitenews.xml?start={}'

    __FILE_CACHE__ = 'cache/moex.pickle'

    def __init__(self) -> None:
      self.__cache__ = self.read_cache()

    def stocks_prices_today(self, params = {}):
      return self.get(self.STOCKS_LIST_URL, params)
    
    def stock_prices(self, security, params = {}):
      return self.get(self.STOCKS_LIST_URL + '/' + security, params)
    
    def index_list(self, params = {}):
      return self.get(self.INDEXES_LIST_URL, params)
    
    def index_prices(self, security, params = {}):
      return self.get(self.INDEXES_LIST_URL + '/' + security, params)
    
    def securities_list(self, index):
      return self.get(self.TICKERS_BY_INDEX.format(index), { 'date': minus_today(1) })
    
    def prices_today(self):
      return self.get()
    
    def get(self, link, params = {}):
      response = self.fetch_cache(link, params)
      if response != None:
        return response

      response = requests.get(link + '?' + urllib.parse.urlencode(params))
      self.write_cache(link, params, xmltodict.parse(response.content))
      return self.fetch_cache(link, params)
    
    def fetch_cache(self, link, params):
      params = json.dumps(params)
      try:
        return self.__cache__[minus_today(0)][link + ' + ' + params]
      except:
        return None
      
    def write_cache(self, link, params, value):
      params = json.dumps(params)
      try:
        self.__cache__[minus_today(0)]
      except:
        self.__cache__[minus_today(0)] = {}
      self.__cache__[minus_today(0)][link + ' + ' + params] = value
      with open(self.__FILE_CACHE__, 'wb') as handle:
        pickle.dump(self.__cache__, handle, protocol=pickle.HIGHEST_PROTOCOL)
      
    def read_cache(self):
      try:
        with open(self.__FILE_CACHE__, 'rb') as handle:
          return pickle.load(handle)
      except:
        return {}
  
  class Parser():
    def __init__(self, client):
      self.client = client
      self.__cache__ = {}

    def today_prices(self):
      data_info = self.get_data(self.client.stocks_prices_today(), 0)
      data_trade = self.get_data(self.client.stocks_prices_today(), 1)
      stocks = {}
      pos = 0
      while pos < len(data_info):
        stocks[data_info[pos]['@SECID']] = {
          'name': data_info[pos]['@SHORTNAME'],
          'open': data_trade[pos]['@OPEN'],
          'close': data_trade[pos]['@LAST'],
          'high': data_trade[pos]['@HIGH'],
          'low': data_trade[pos]['@LOW'],
          'capitalization': data_trade[pos]['@ISSUECAPITALIZATION']
        }
        pos += 1
      return stocks

    def moex_indexes(self):
      start = 0
      get_indexes = lambda start: self.get_data(self.client.index_list({ 'start': start, 'date': minus_today(1) }))
      data = get_indexes(start)
      indexes = {}
      while data:
        for block in data:
          index = block['@SECID']
          capitalization = block['@CAPITALIZATION']
          if 'MOEX' in index and capitalization:
            indexes[index] = {
              'name': block['@SHORTNAME'],
              'capitalization': capitalization,
              'tickers': self.securities_list(index)
            }
        start += 100
        data = get_indexes(start)
      
      return indexes
    
    def indexes_changes(self, indexes_dict, days_ranges = [7, 14, 30, 90]):
      for index in indexes_dict:
        get_prices = lambda days: self.get_data(self.client.index_prices(index, { 'from': minus_today(days) }))
        prices = get_prices(max(days_ranges))
        indexes_dict[index]['changes'] = {}
        for days in days_ranges:
          indexes_dict[index]['changes'][days] = str(self.__changes__(prices, days)) + '%'
      
      return indexes_dict
    
    def securities_list(self, index):
      return [row['@ticker'] for row in self.get_data(self.client.securities_list(index))]

    def __changes__(self, prices, days):
      prices = prices[-days:]
      low = min([float(row['@LOW']) for row in prices])
      high = max([float(row['@HIGH']) for row in prices])
      last_close = float(prices[-1]['@CLOSE'])
      changes = [round((1 - low/last_close) * 100, 2), round(-(1-last_close/high) * 100, 2)]
      if changes[0] > abs(changes[1]):
        return changes[0]
      else:
        return changes[1]
      
    def get_data(self, response, data_position = 0):
      try:
        return response['document']['data']['rows']['row']
      except:
        if response['document']['data'][data_position]['rows'] == None:
          return None
        return response['document']['data'][data_position]['rows']['row']
  