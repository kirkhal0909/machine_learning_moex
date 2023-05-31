from app.api.client import Client

class BCSClient(Client):
  __DIVIDENDS_CALENDAR_LINK__ = 'https://api.bcs.ru/divcalendar/v1/dividends?actual={}&limit=1000&order=2&sorting=0'

  __FILE_CACHE__ = 'cache/bcs.pickle'

  def dividends_data(self, actual = True):
    actual_param = str(int(actual))
    print(self.__DIVIDENDS_CALENDAR_LINK__.format(actual_param))
    return self.get(self.__DIVIDENDS_CALENDAR_LINK__.format(actual_param), request_type='json')