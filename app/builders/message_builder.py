class Message():
    @staticmethod
    def indexes_to_text(indexes):
      messages = []
      for index in indexes:
        data = indexes[index]
        message = Message.format_long_number(data['capitalization']) + '\n'
        message += " {} - {}".format(index, data['name'])
        message += '\n\n'
        for day in data['changes']:
          message += " {}: {}% {}\n".format(day, data['changes'][day][0], Message.format_long_number(data['changes'][day][1]))
        message += '\n\n'
        for ticker in data['tickers']:
          message += "   {}\n".format(ticker)
          for day in data['tickers'][ticker]['changes']:
            message += "    {}: {}% {}\n".format(day, data['tickers'][ticker]['changes'][day][0], Message.format_long_number(data['tickers'][ticker]['changes'][day][1]))
        message += '\n-----------------------'
        messages.append(message)
         
      return messages

    @staticmethod
    def format_long_number(number):
      return "{:,}".format(int(float(number)))