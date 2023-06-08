from app.helpers.dates import minus_today

class MOEXTensorflowData():
  def __init__(self, client):
    self.client = client

  def get_data(self, response, data_position = 0):
    try:
      return response['document']['data']['rows']['row']
    except:
      if response['document']['data'][data_position]['rows'] == None:
        return None
      return response['document']['data'][data_position]['rows']['row']

  def stocks_prices_all_period(self, ticker):
    data_by_dates = {}
    days = 0
    get_date = lambda prices_row: prices_row.get('@TRADEDATE') or prices_row.get('@SYSTIME').split(' ')[0]
    prices = [row for row in self.get_data(self.client.stocks_prices_today(), 1) if row['@SECID'] == ticker]

    while not data_by_dates.get(get_date(prices[0])):
      imoex = self.get_data(self.client.index_prices('IMOEX', { 'from': minus_today(days) }), 0)
      for row in prices:
        data_by_dates[get_date(row)] = {
          'open': row['@OPEN'],
          'close': row.get('@CLOSE') or row.get('@MARKETPRICE'),
          'high': row['@HIGH'],
          'low': row['@LOW'],
          'volume': row.get('@VOLUME') or row['@VOLTODAY'],
          'value_traded': row.get('@MP2VALTRD') or row['@VALTODAY'],
        }
      for row in [imoex] if imoex.__class__ == dict else imoex:
        if data_by_dates.get(get_date(row)):
          data_by_dates[get_date(row)] = {
            **data_by_dates.get(get_date(row)),
            'imoex_open': row.get('@OPEN'),
            'imoex_close': row.get('@CLOSE'),
            'imoex_high': row.get('@HIGH'),
            'imoex_low': row.get('@LOW'),
            'imoex_value': row.get('@VALUE'),
            'imoex_capitalization': row.get('@CAPITALIZATION')
          }
      days += 90
      prices = self.get_data(self.client.stock_prices(ticker, { 'from': minus_today(days) }), 1)

    return data_by_dates
