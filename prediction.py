import numpy as np
import pandas as pd

from app.api.moex.moex import MOEX
from app.helpers.dates import now

moex = MOEX()

config = {
  'model_type': 'Classification', # or 'LSTM'
  'epochs': 10,
  'normalization_type': 'candles', # or 'candles'
  'input_range': 30,
  'model_neurons1': 64,
  'model_neurons2': None,
  'data_length': None,
  'load_model': False,
}

filename = "_info/_results_{}.txt".format(now())

for model_neurons1 in [16, 32, 64, 128, 256]:
  for input_range in [30, 24, 20, 16, 8]:

    config['model_neurons1'] = model_neurons1
    config['input_range'] = input_range

    moex.ml.update_configs(config)

    x, y, model = moex.ml.fit()
    y_unscale = moex.ml.data_fit.unscale(y)
    y_p = moex.ml.predict(x)


    eq_direction = 0

    for pos in range(len(y)):
        y_p_positive = y_p[pos][1] > y_p[pos][0]
        if y_unscale[pos] <= 0 and not y_p_positive:
            eq_direction += 1
        elif y_unscale[pos] > 0 and y_p_positive:
            eq_direction += 1

    results_file = open(filename, 'a')

    for key in config:
        results_file.write("{}: {}\n".format(key, config[key]))

    results = "{} / {}\n\n\n".format(eq_direction, len(y_unscale))
    print(moex.ml.config)
    print(results)

    results_file.write(results)
    results_file.close()
