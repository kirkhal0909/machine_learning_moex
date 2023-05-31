from app.helpers.dictionaries import first_key

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
          if data_ticker.get('percent'):
            days = first_key(data_ticker['changes'])
            dividend_value = round(data_ticker['changes'][days][1] / 100 * data_ticker.get('percent'), 2)
            mark_highlight = '✓' if dividend_value > 400_000_000 else ''
          else:
            dividend_value = 0
            mark_highlight = ''
          message += "   {}{}".format(ticker, ' {}                   дивиденды: {}% ({}) {}\n'.format(mark_highlight, data_ticker.get('percent'), data_ticker.get('last_buy_day'), Message.format_long_number(dividend_value)) if data_ticker.get('percent') else '\n')
          for day in data_ticker['changes']:
            message += "    {}: {}% {}\n".format(day, data_ticker['changes'][day][0], Message.format_long_number(data_ticker['changes'][day][1]))
        message += '\n-----------------------'
        messages.append(message)
         
      return messages

    @staticmethod
    def format_long_number(number):
      return "{:,}".format(int(float(number)))