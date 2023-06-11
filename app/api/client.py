from curl_cffi import requests
import xmltodict
import json
import urllib

import pickle

from app.helpers.dates import minus_today

from io import StringIO
import csv

class Client():
  __FILE_CACHE__ = 'cache/client_cache.pickle'
  def __init__(self) -> None:
    self.__cache__ = self.read_cache()

  def get(self, link, params = {}, cache = True, request_type='xml'):
    response = self.fetch_cache(link, params)
    if response != None and cache:
      return response

    print(" GET {} {}".format(link, params))
    
    link_params = urllib.parse.urlencode(params)
    link_params = "?{}".format(link_params) if link_params else link_params
    response = requests.get(link + link_params)
    content = self.__content__(response, request_type)
    self.write_cache(link, params, content)
    return self.fetch_cache(link, params)

  def __content__(self, response, request_type):
    if request_type == 'xml':
      return xmltodict.parse(response.content)
    elif request_type == 'json':
      return response.json()
    elif request_type == 'csv':
      csv_file = StringIO(response.content.decode('cp1251'))
      return [row for row in csv.reader(csv_file, delimiter=';')]
    elif request_type == 'html':
      return response.text
    else:
      return response.content

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
