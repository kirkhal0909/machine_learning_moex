class BCSParser():
  def __init__(self, client) -> None:
    self.client = client

  def dividends_data(self, actual=True):
    tickers = {}
    response = self.client.dividends_data(actual)['data']
    for row in response:
      tickers[row['secure_code']] = {
        'percent': row['yield'],
        'last_buy_day': self.__cut_date__(row['last_buy_day']),
        'closing_date': self.__cut_date__(row['closing_date'])
      }
    return tickers
  
  def ticker_data(self, ticker):
    return self.dividends_data().get(ticker) or self.dividends_data(False).get(ticker) or {}
  
  def __cut_date__(self, date):
    if date:
      return date.split('T')[0]