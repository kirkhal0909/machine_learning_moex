from app.helpers.dates import minus_today
from app.helpers.dictionaries import first_key

class MOEXParser():
  def __init__(self, client):
    self.client = client
    self.__cache__ = {}

  def today_prices(self):
    response = self.client.stocks_prices_today()
    data_info = self.get_data(response, 0)
    data_trade = self.get_data(response, 1)
    stocks = {}
    pos = 0
    while pos < len(data_info):
      stocks[data_info[pos]['@SECID']] = {
        'name': data_info[pos]['@SHORTNAME'],
        'open': data_trade[pos]['@OPEN'],
        'close': data_trade[pos]['@LAST'],
        'high': data_trade[pos]['@HIGH'],
        'low': data_trade[pos]['@LOW'],
        'change': data_trade[pos]['@CHANGE'],
        'capitalization': data_trade[pos]['@ISSUECAPITALIZATION']
      }
      pos += 1
    return stocks
  
  def stocks_prices(self, tickers, days_ranges = [7, 14, 30, 90]):
    tickers_data = {}
    for ticker in tickers:
      prices = self.get_data(self.client.stock_prices(ticker, { 'from': minus_today(max(days_ranges)) }), 1)
      tickers_data[ticker] = { 'changes': {} }
      for days in days_ranges:
        tickers_data[ticker]['changes'][days] = self.__changes__(prices, days)
    return self.sort_tickers_data(tickers_data)
  
  def sort_tickers_data(self, tickers_data):
    sorted_data = sorted((tickers_data.items()), key=lambda ticker:ticker[1]['changes'][first_key(ticker[1]['changes'])] )
    return dict(sorted_data)

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
            'tickers': self.stocks_prices(self.securities_list(index))
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
        indexes_dict[index]['changes'][days] = self.__changes__(prices, days)
    
    return self.sort_tickers_data(indexes_dict)
  
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
