from app.api.smart_lab.smart_lab_client import SmartLabClient
from bs4 import BeautifulSoup

class SmartLabParser():
  def __init__(self, client) -> None:
    self.client = client

  def reports(self, ticker = 'all'):    
    try:
      if ticker == 'all':
        return self.__report_data__
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
      indexes_table = [1, -7, -6, -5, -4, -1]
      self.__report_data__ = {}
      for pos_table in range(2):
        for pos_row in range(1, len(tables[pos_table]), 1):
          row = tables[pos_table][pos_row]
          self.__report_data__[row[indexes_table[0]]] = {
            'profit': row[indexes_table[1]],
            'changes_quarter': row[indexes_table[2]] if len(row[indexes_table[2]]) > 1 else None,
            'changes_year': row[indexes_table[3]] if len(row[indexes_table[3]]) > 1 else None,
            'report': row[indexes_table[4]],
            'report_date': row[indexes_table[5]],
          }

    if ticker == 'all':
      return self.__report_data__
    else:
      return self.__report_data__.get(ticker)
    