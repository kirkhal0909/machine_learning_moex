from app.api.moex.moex import MOEX

moex = MOEX()
x, y, model = moex.ml.fit()
y_unscale = moex.ml.data_fit.unscale(y)
y_p = moex.ml.predict(x)


eq_direction = 0

for pos in range(len(y)):
    if y_unscale[pos] < 0 and float(y_p[pos]) < 0:
        eq_direction += 1
    elif y_unscale[pos] >= 0 and float(y_p[pos]) >= 0:
        eq_direction += 1

print("{} / {}".format(eq_direction, len(y_unscale)))
