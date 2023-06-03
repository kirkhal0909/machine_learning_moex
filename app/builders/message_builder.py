from app.helpers.dictionaries import first_key
from app.helpers.dates import date

class Message():
  @staticmethod
  def indexes_to_text(indexes):
    messages = []
    for index in indexes:
      data = indexes[index]
      message = "{} - {} {}\n".format(index, data['name'], Message.format_long_number(data['capitalization']))
      for day in data['changes']:
        message += " {}: {}% {}\n".format(day, data['changes'][day][0], Message.format_long_number(data['changes'][day][1]))
      message += '\n\n'
      for ticker in data['tickers']:
        data_ticker = data['tickers'][ticker]
        if data_ticker.get('report'):
          message += "   {}\n".format(Message.report_info(data_ticker))
        message += "   {} {} {} {} {}".format(
          data_ticker['level'], 
          ticker,
          Message.format_long_number(data_ticker.get('capitalization')) if data_ticker.get('capitalization') else '', 
          data_ticker.get('name'), ' {}                   дивиденды: {}% ({}) {}\n'.format(
            data_ticker.get('mark_highlight'), 
            data_ticker.get('percent'), 
            data_ticker.get('last_buy_day'), 
            Message.format_long_number(data_ticker.get('dividend_value'))
          ) if data_ticker.get('percent') else '\n'
        )
        for day in data_ticker['changes']:
          message += "      {}: {}% {}\n".format(day, data_ticker['changes'][day][0], Message.format_long_number(data_ticker['changes'][day][1]))
        message += '\n'
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
  
  @staticmethod
  def reports(data):
    message = ''
    sorted_data = dict(sorted(data.items(), key=lambda data_reports:date(data_reports[1]['report_date'])))
    for ticker in sorted_data:
      message += '{} {}\n'.format(ticker.ljust(5), Message.report_info(data[ticker]))
    return message

  def false_breakoutes(data):
    message = ''
    changes = {}
    for ticker in data:
      if data[ticker]['false_breakout'][-1]:
        changes[ticker] = Message.changes_next(data[ticker], -2)

    changes = dict(sorted(changes.items(), key=lambda data:data[1]))
    for ticker in changes:  
      message += "{} {} breakout {}%\n".format(data[ticker].get('level'), ticker, round(changes[ticker], 2))
    return message
  
  def changes_next(data_ticker, position_left):
    if len(data_ticker['close']) <= position_left:
      return 0
    close_left = float(data_ticker['close'][position_left])
    close_right = float(data_ticker['close'][position_left + 1])
    if close_left < close_right:
      return (1 - close_left / close_right) * 100
    else:
      return -(1 - close_right / close_left) * 100
  
  def sequence_false_breakouts(data):
    message = ''
    for ticker in data:
      message += "{} {}".format(data[ticker]['level'], ticker)
      for position in range(len(data[ticker])):
        if data[ticker]['false_breakout'][position]:
          message +=  " {};".format(data[ticker]['dates'][position])
      message += '\n'
    return message