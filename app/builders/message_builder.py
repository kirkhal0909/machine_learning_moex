class Message():
    @staticmethod
    def indexes_to_text(indexes):
      messages = []
      for index in indexes:
        data = indexes[index]
        message = "{:,}\n".format(float(data['capitalization']))
        message += " {} - {}".format(index, data['name'])
        message += '\n\n'
        for day in data['changes']:
          message += " {}: {}%\n".format(day, data['changes'][day])
        message += '\n\n'
        for ticker in data['tickers']:
          message += "   {}\n".format(ticker)
          for day in data['tickers'][ticker]['changes']:
            message += "    {}: {}%\n".format(day, data['tickers'][ticker]['changes'][day])
        message += '\n-----------------------'
        messages.append(message)
         
      return messages