from app.helpers.dates import minus_today
from app.api.client import Client

class MOEXClient(Client):
  STOCKS_LIST_URL = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities'
  STOCKS_HISTORY_URL = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities'
  INDEXES_LIST_URL = 'https://iss.moex.com/iss/history/engines/stock/markets/index/securities'
  TICKERS_BY_INDEX = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/{}/tickers'
  MOEX_NEWS_LINK = 'https://iss.moex.com/iss/sitenews.xml?start={}'

  __FILE_CACHE__ = 'cache/moex.pickle'

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