import app.helpers.dates
import requests
import json
import pickle
import os

class BankClient():
  __FILE_DATA_PATH__ = "cache/{}.pickle"
  __DATA__ = None

  def __init__(self):
    self.data()

  def get(self, url):
    self.RESPONSE = requests.get(url)
    return self.RESPONSE

  def get_content(self, url):
    return self.get(url).content

  def get_json(self, url):
    return self.get(url).json()

  def get_text(self, url):
    return self.get(url).text

  def get_substring(self, left_string, right_string, from_pos = 0):
    return self.__search_substring__(self.RESPONSE.text, left_string, right_string, from_pos)

  def get_json_substring(self, left_string, right_string):
    return json.loads(self.get_substring(left_string, right_string))

  def __search_substring__(self, string, left_part, right_part, from_pos = 0):
    left_pos = string.find(left_part, from_pos) + len(left_part)
    right_pos = string.find(right_part, left_pos)
    return string[left_pos:right_pos]

  def __cut_dates__(self, data):
    last_key_rate = None
    cutted = {
      "dates": [],
      "key_rates": []
    }
    for pos in range(len(data['dates'])):
      date = app.helpers.dates.date(data['dates'][pos])
      key_rate = data['key_rates'][pos]
      if key_rate != last_key_rate:
        last_key_rate = key_rate
        cutted['dates'].append(date)
        cutted['key_rates'].append(key_rate)
    return cutted

  def data(self):
    if not self.__DATA__:
      self.__read_data__()
      if self.__data_old__():
        self.__DATA__ = self.__cut_dates__(self.__load_data__())
        self.__DATA__['bank'] = self.__human_name__()
        self.__DATA__['actual_date'] = app.helpers.dates.today()
        try:
          self.__DATA__ |= self.__load_inflation_data__()
        except:
          print("BANKS: Some error with download inflation_data {}".format(self.__class__.__name__))
        self.__write_data__()
    return self.__DATA__

  def __human_name__(self):
    try:
      return self.__BANK_NAME__
    except:
      return self.__class__.__name__

  def __data_old__(self):
    if not self.__DATA__:
      return True
    key = 'actual_date'
    if key not in self.__DATA__.keys():
      return True

    return self.__DATA__[key] != app.helpers.dates.today()

  def __read_data__(self):
    try:
      with open(self.__file_path__(), 'rb') as handle:
        self.__DATA__ = pickle.load(handle)
    except:
      None

  def __write_data__(self):
    try:
      dirname = os.path.dirname(self.__file_path__())
      if os.path.exists(dirname) == False:
        os.makedirs(dirname)
      with open(self.__file_path__(), 'wb') as handle:
        pickle.dump(self.__DATA__, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except:
      None

  def __file_path__(self):
    return self.__FILE_DATA_PATH__.format(self.__class__.__name__)

  def __load_data__(self) -> dict:
    pass

  def __load_inflation_data__(self) -> dict:
    return {}

  def inflation_by(self, date):
    if 'inflations' not in self.__DATA__.keys():
      return 0
    return self.__value_by__(date, 'inflations', 'inflations_dates')

  def inflations_by(self, dates):
    return [self.inflation_by(date) for date in dates]

  def key_rate_by(self, date):
    return self.__value_by__(date, 'key_rates', 'dates')

  def key_rates_by(self, dates):
    return [self.key_rate_by(date) for date in dates]

  def __value_by__(self, date, key, date_key):
    date = app.helpers.dates.date(date)
    pos = 0
    while pos < len(self.__DATA__[date_key]) - 1:
      if date < app.helpers.dates.date(self.__DATA__[date_key][pos + 1]):
        break
      pos += 1
    return self.__DATA__[key][pos]

  def __values_by__(self, dates, key, date_key):
    return [self.__value_by__(date, key, date_key) for date in dates]

