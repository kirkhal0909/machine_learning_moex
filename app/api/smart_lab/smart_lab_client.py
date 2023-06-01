from app.api.client import Client

class SmartLabClient(Client):
  REPORTS_LINK = 'https://smart-lab.ru/q/shares_fundamental3/'

  def reports(self):
    return self.get(self.REPORTS_LINK, request_type='html')
    