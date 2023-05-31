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
          data_ticker = data['tickers'][ticker]
          message += "   {}{}".format(ticker, '                     дивиденды: {}% ({})\n'.format(data_ticker.get('percent'), data_ticker.get('last_buy_day')) if data_ticker.get('percent') else '\n')
          for day in data_ticker['changes']:
            message += "    {}: {}% {}\n".format(day, data_ticker['changes'][day][0], Message.format_long_number(data_ticker['changes'][day][1]))
        message += '\n-----------------------'
        messages.append(message)
         
      return messages

    @staticmethod
    def format_long_number(number):
      return "{:,}".format(int(float(number)))