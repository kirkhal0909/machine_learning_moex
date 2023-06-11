from app.api.moex.moex import MOEX

from app.neural_network.ticker_prediction import TickerPrediction

moex = MOEX()
tomorrow_sber, model, x, y, last_sequence, _normalized_dataframe = TickerPrediction().predict_tomorrow_close('SBER')
