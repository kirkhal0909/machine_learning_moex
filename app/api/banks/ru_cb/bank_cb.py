from app.api.banks.bank_client import BankClient
import openpyxl
import io

class BankСb(BankClient):
  __BANK_CB_URL__ = 'https://www.cbr.ru/hd_base/KeyRate/'
  __BANK_CB_INFLATION__ = 'https://www.cbr.ru/Queries/UniDbQuery/DownloadExcel/132934?Posted=True&From=17.09.2013&To=05.05.2023&FromDate=09%2F17%2F2013&ToDate=01%2F01%2F2170'
  __BANK_NAME__ = 'ЦБ РФ'

  def __load_data__(self):
    self.get_text(self.__BANK_CB_URL__)
    data = {
      "dates": self.get_json_substring('"categories":', ',"t'),
      "key_rates": self.get_json_substring('"data":', ',"c')
    }
    return data

  def __load_inflation_data__(self):
    inflations_dates = []
    inflations = []
    xlsx = io.BytesIO(self.get_content(self.__BANK_CB_INFLATION__))
    wb = openpyxl.load_workbook(xlsx)
    ws = wb.worksheets[0]

    for row in list(ws.iter_rows(values_only=True))[::-1]:
      if row[1].__class__ == str:
        continue
      inflations_dates.append(row[0])
      inflations.append(row[2])

    return {
      "inflations_dates": inflations_dates,
      "inflations": inflations
    }

