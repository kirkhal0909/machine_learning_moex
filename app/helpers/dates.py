from datetime import datetime, timedelta

def date(date_argument):
  if date_argument.__class__ == str:
    if '.' in date_argument:
      if date_argument.count('.') == 1:
        date_argument = "01." + date_argument
      dd, mm, yy = date_argument.split('.')
      date_argument = "{}-{}-{}".format(yy, mm, dd)
    return datetime.fromisoformat(date_argument.split('T')[0])
  if date_argument.__class__ in [int, float]:
    return datetime.fromtimestamp(int(date_argument))
  else:
    return date_argument
  
def today():
  return datetime.today().date()

def today_str():
  return today().strftime('%Y-%m-%d')

def minus_days(date, days):
  return date - timedelta(days=days)

def minus_today(days):
  return minus_days(today(), days).strftime('%Y-%m-%d')

