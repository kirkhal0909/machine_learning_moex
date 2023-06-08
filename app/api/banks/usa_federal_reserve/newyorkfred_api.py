from app.api.banks.bank_client import BankClient
import json

class NewyorkfredAPI(BankClient):
  __NEWYORKFED_URL__ = 'https://markets.newyorkfed.org/read?productCode=50&eventCodes=500&startDt=2010-07-03&endDt=2023-05-05&fields=dailyRate,tradingVolume,refRateDt,targetRateFrom,targetRateTo&sort=postDt:1'
  __BANK_NAME__ = 'FEDERAL RESERVE SYSTEM'

  def __load_data__(self):
    data = {
      "dates": [],
      "key_rates": []
    }
    for block in self.get_json(self.__NEWYORKFED_URL__)['data']:
      json_data = json.loads(block['data'])
      data['dates'].append(json_data['refRateDt'])
      data['key_rates'].append(json_data['dailyRate'])
    return data
