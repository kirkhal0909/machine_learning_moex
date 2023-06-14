from app.api.moex.moex import MOEX

moex = MOEX()
ticker = 'SBER'
x, y, model = moex.ml.fit(ticker)
