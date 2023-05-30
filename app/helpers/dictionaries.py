def first_key(dict_argument, sort_up=True):
  return sorted(list(dict_argument.keys()), reverse = sort_up == False)[0]