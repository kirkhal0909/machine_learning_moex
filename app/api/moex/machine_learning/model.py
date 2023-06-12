from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import keras
from keras.callbacks import ModelCheckpoint

class Model():
  def __init__(self, model_version = 1) -> None:
    self.__model_path__ = 'models/moex.h5'
    self.__model_version__ = model_version

  def model(self, input_shape):
    model = Sequential()

    if self.__model_version__ == 1:
      model.add(LSTM(64, return_sequences=True, input_shape=input_shape ))
      model.add(Dropout(0.3))
      model.add(LSTM(120, return_sequences=False))
      model.add(Dropout(0.3))
      model.add(Dense(20))
      model.add(Dense(1, activation='linear'))
    elif self.__model_version__ == 2:
      model.add(LSTM(units=64, return_sequences=True, input_shape=input_shape))
      model.add(LSTM(units=10, return_sequences=False))
      model.add(Dropout(0.25))
      model.add(Dense(units=1, activation='linear'))

    model.compile(optimizer = keras.optimizers.Adam(learning_rate=0.01), loss='mean_squared_error')
    return model

  def fit(self, x_train, y_train, batch_size = 512, epochs = 64):
    try:
      self.__model__
    except AttributeError:
      self.__model__ = self.model(x_train[0].shape)
    # es = EarlyStopping(monitor='val_loss', min_delta=1e-10, patience=10, verbose=1)
    # rlr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, verbose=1)
    mcp = ModelCheckpoint(filepath=self.__model_path__, monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=True)
    self.__model__.fit(
      x_train,
      y_train,
      shuffle=True,
      callbacks=[mcp],
      validation_split=0.2,
      verbose=1,
      batch_size=batch_size,
      epochs=epochs
    )

    self.__model__.summary()

    return self.__model__
