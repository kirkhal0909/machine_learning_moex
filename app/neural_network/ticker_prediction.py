from app.api.moex.moex import MOEX

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout


class TickerPrediction():
  __INPUT_LENGTH__ = 7
  __BATCH_SIZE__ = 8
  __EPOCHS__ = 8

  def __init__(self) -> None:
    self.moex = MOEX()
    self.tensorflow_data = self.moex.tensorflow_data

  def predict_tomorrow_close(self, ticker):
    x, y, last_sequence, _normalized_dataframe = self.tensorflow_data.get_x_y(ticker)
    model = self.model(x, y)
    prediction = model.predict(last_sequence)
    return prediction, model, x, y, last_sequence, _normalized_dataframe

  def model(self, x_train, y_train):
    model = Sequential()
    x_train = x_train
    y_train = y_train
    model.add(LSTM(60, return_sequences=True, input_shape=x_train[0].shape ))
    model.add(Dropout(0.3))
    model.add(LSTM(120, return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(20))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')

    model.fit(x_train, y_train,
              batch_size=self.__BATCH_SIZE__,
              epochs=self.__EPOCHS__,
              verbose=1)

    model.summary()

    return model
