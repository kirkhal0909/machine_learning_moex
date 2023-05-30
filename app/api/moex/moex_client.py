from curl_cffi import requests
import xmltodict
import json
import urllib

import pickle

from app.helpers.dates import minus_today

class MOEXClient():
  STOCKS_LIST_URL = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities'
  STOCKS_HISTORY_URL = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities'
  INDEXES_LIST_URL = 'https://iss.moex.com/iss/history/engines/stock/markets/index/securities'
  TICKERS_BY_INDEX = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/{}/tickers'
  MOEX_NEWS_LINK = 'https://iss.moex.com/iss/sitenews.xml?start={}'

  __FILE_CACHE__ = 'cache/moex.pickle'

  def __init__(self) -> None:
    self.__cache__ = self.read_cache()

  def stocks_prices_today(self, params = {}):
    return self.get(self.STOCKS_LIST_URL, params, cache = False)
  
  def stock_prices(self, security, params = {}):
    return self.get(self.STOCKS_HISTORY_URL + '/' + security, params)
  
  def index_list(self, params = {}):
    return self.get(self.INDEXES_LIST_URL, params)
  
  def index_prices(self, security, params = {}):
    return self.get(self.INDEXES_LIST_URL + '/' + security, params)
  
  def securities_list(self, index):
    return self.get(self.TICKERS_BY_INDEX.format(index), { 'date': minus_today(1) })
  
  def prices_today(self):
    return self.get()
  
  def get(self, link, params = {}, cache = True):
    response = self.fetch_cache(link, params)
    if response != None and cache:
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
      self.__cache__ = { minus_today(0): {}}
    self.__cache__[minus_today(0)][link + ' + ' + params] = value
    with open(self.__FILE_CACHE__, 'wb') as handle:
      pickle.dump(self.__cache__, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
  def read_cache(self):
    try:
      with open(self.__FILE_CACHE__, 'rb') as handle:
        return pickle.load(handle)
    except:
      return {}
