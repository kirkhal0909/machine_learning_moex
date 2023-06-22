import numpy as np
import pandas as pd

from app.api.moex.moex import MOEX

moex = MOEX()

config = {
  'model_type': 'Classification', # or 'LSTM'
  'epochs': 1,
  'normalization_type': 'candles', # or 'candles'
  'input_range': 30,
  'model_neurons1': 64,
  'model_neurons2': None,
  'data_length': None,
  'load_model': True,
  'batch_size': 1024
}

for input_range in range(32, 0, -1):
  for model_neurons1 in range(1, 513, 1):
    rewrite_model = True
    min_predicted = 999_999_999_999_999_999
    max_predicted = 0
    for retries in range(10):
      config['model_neurons1'] = model_neurons1
      config['input_range'] = input_range

      moex.ml.update_configs(config)

      x, y, model = moex.ml.fit(rewrite_model=rewrite_model)
      rewrite_model = False
      y_unscale = moex.ml.data_fit.unscale(y)
      y_p = moex.ml.predict(x)

      eq_direction = 0
      for pos in range(len(y)):
          positive1 = y_p[pos][1] > y_p[pos][0]
          positive2 = y_unscale[pos][0] == 1
          if positive1 == positive2:
            eq_direction += 1
      results = "{} / {}\n\n\n".format(eq_direction, len(y_unscale))

      print(moex.ml.config)
      print(results)

      if eq_direction < min_predicted or eq_direction > max_predicted:
         moex.ml.model.copy("{}_{}_{}".format(eq_direction, model_neurons1, input_range))

      if eq_direction < min_predicted:
         min_predicted = eq_direction
      if eq_direction > max_predicted:
         max_predicted = eq_direction
