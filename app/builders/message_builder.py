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
        if data_ticker.get('report'):
          message += "   {}\n".format(Message.report_info(data_ticker))
        message += "   {} {}{}".format(data_ticker['level'], ticker, ' {}                   дивиденды: {}% ({}) {}\n'.format(
            data_ticker.get('mark_highlight'), 
            data_ticker.get('percent'), 
            data_ticker.get('last_buy_day'), 
            Message.format_long_number(data_ticker.get('dividend_value'))) if data_ticker.get('percent') else '\n'
          )
        for day in data_ticker['changes']:
          message += "      {}: {}% {}\n".format(day, data_ticker['changes'][day][0], Message.format_long_number(data_ticker['changes'][day][1]))
      message += '\n-----------------------'
      messages.append(message)
        
    return messages

  @staticmethod
  def format_long_number(number):
    return "{:,}".format(int(float(number)))
  
  @staticmethod
  def report_info(data_ticker):
    report, report_date, profit, changes_quarter, changes_year = [ data_ticker.get(key) for key in ['report', 'report_date', 'profit', 'changes_quarter', 'changes_year'] ]
    message = "{}{}{}{}{}".format(
            report if report else '',
            " ({})".format(report_date) if report_date else '',
            " (прибыль {} млрд)".format(profit) if profit else '',
            " (квартал {})".format(changes_quarter) if changes_quarter else '',
            " (год {})".format(changes_year) if changes_year else '',
          )
    return message
  
  @staticmethod
  def calendar_minus_energy(indexes):
    calendar = {}
    for index in indexes:
      for ticker in indexes[index]['tickers']:
        data_ticker = indexes[index]['tickers'][ticker]
        if data_ticker.get('last_buy_day'):
          calendar[ticker] = {
            'mark_highlight': data_ticker.get('mark_highlight'),
            'percent': data_ticker.get('percent'),
            'last_buy_day': data_ticker.get('last_buy_day'),
            'value': data_ticker['changes'][first_key(data_ticker['changes'])][1],
            'data_ticker': data_ticker
          }
    calendar = dict(sorted(calendar.items(), key=lambda data:data[1]['last_buy_day']))

    message = ''
    for ticker in calendar:
      data = calendar[ticker]
      message += '{} {} - {} (дивиденды {}%); \t{}\n'.format(
        data['last_buy_day'], 
        ticker.ljust(5), 
        Message.format_long_number(data['value']).ljust(15), 
        data['percent'],
        Message.report_info(data.get('data_ticker'))
      )
    return message