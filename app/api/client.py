from curl_cffi import requests
import xmltodict
import json
import urllib

import pickle

from app.helpers.dates import minus_today

class Client():
  __FILE_CACHE__ = 'cache/client_cache.pickle'
  def __init__(self) -> None:
    self.__cache__ = self.read_cache()
    
  def get(self, link, params = {}, cache = True, request_type='xml'):
    response = self.fetch_cache(link, params)
    if response != None and cache:
      return response

    link_params = urllib.parse.urlencode(params)
    link_params = "?{}".format(link_params) if link_params else link_params
    response = requests.get(link + link_params)
    if request_type == 'xml':
      content = xmltodict.parse(response.content)
    elif request_type == 'json':
      content = response.json()
    else:
      content = response.content
    self.write_cache(link, params, content)
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
