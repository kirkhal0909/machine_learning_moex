from app.api.smart_lab.smart_lab_client import SmartLabClient
from bs4 import BeautifulSoup

class SmartLabParser():
  def __init__(self, client) -> None:
    self.client = client

  def reports(self, ticker):
    try:
      return self.__report_data__.get(ticker)
    except:
      response = self.client.reports()
      soup = BeautifulSoup(response, 'lxml')
      soup_tables = soup.find_all('table')
      tables = [
        [
          [
            (column.find('a', href=True) or { 'href': '' }).get('href').split('/')[-1] or
            ' '.join(column.findAll(text=True))  for column in row.find_all(['td','th'])
          ] for row in table.findAll('tr')
        ] for table in soup_tables
      ]
      indexes_tables = [
        [ tables[0][0].index(name) for name in ['Тикер', 'Чистая прибыль', 'Изм,  % к/к', 'Изм,  % г/г', 'отчет', 'дата публикации']],
        [ tables[1][0].index(name) for name in ['Название', 'Чистая прибыль', 'Изм,  % к/к', 'Изм,  % г/г', 'отчет', 'дата публикации']]
      ]
      self.__report_data__ = {}
      for pos_table in range(2):
        indexes_table = indexes_tables[pos_table]
        for row in tables[pos_table]:
          self.__report_data__[row[indexes_table[0]]] = {
            'profit': row[indexes_table[1]],
            'changes_quarter': row[indexes_table[2]] if len(row[indexes_table[2]]) > 1 else None,
            'changes_year': row[indexes_table[3]] if len(row[indexes_table[3]]) > 1 else None,
            'report': row[indexes_table[4]],
            'report_date': row[indexes_table[5]],
          }

    return self.__report_data__.get(ticker)
    