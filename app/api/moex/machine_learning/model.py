from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Flatten
import keras
from keras.callbacks import ModelCheckpoint
import os

class Model():
  def __init__(self, model_version = 1, config = {}) -> None:
    self.__model_version__ = model_version
    self.config = config

  def update_config(self, config):
    self.config = {
      config
      **self.config
    }

  def set_config(self, config):
    self.config = config

  def model(self, input_shape=None):
    if os.path.exists(self.__model_path__()) and self.config['load_model'] != False:
      return keras.models.load_model(self.__model_path__())

    model = Sequential()

    neurons1 = self.config['model_neurons1'] or 128
    neurons2 = self.config['model_neurons2'] or int(neurons1 * ( 2 / 3 ))
    if self.config['model_type'] == 'LSTM':
      model.add(LSTM(neurons1, return_sequences=True, input_shape=input_shape ))
      model.add(Dropout(0.3))
      model.add(LSTM(neurons2, return_sequences=False))
      model.add(Dropout(0.3))
    elif self.config['model_type'] == 'Classification':
      model.add(Flatten(input_shape=input_shape))
      model.add(Dense(units=neurons1, activation='relu'))
      model.add(Dense(units=neurons2, activation='relu'))

    if self.config['output_dense'] != 1:
      model.add(Dense(self.config['output_dense'], activation='softmax'))
    else:
      model.add(Dense(1, activation='linear'))

    return model

  def __model_path__(self):
    return 'models/moex_v{}.h5'.format(self.config['model_type'])

  def fit(self, x_train, y_train, batch_size = 128, epochs = 64, rewrite_model = False):
    if rewrite_model:
      self.__model__ = self.model(x_train[0].shape)
    try:
      self.__model__
    except AttributeError:
      self.__model__ = self.model(x_train[0].shape)
    self.__model__.compile(optimizer = keras.optimizers.Adam(learning_rate=0.001), loss='mean_squared_error')
    # es = EarlyStopping(monitor='val_loss', min_delta=1e-10, patience=10, verbose=1)
    # rlr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, verbose=1)
    mcp = ModelCheckpoint(filepath=self.__model_path__(), monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=False)
    self.__model__.fit(
      x_train,
      y_train,
      shuffle=True,
      callbacks=[mcp],
      validation_split=0.2,
      verbose=1,
      batch_size=self.config['batch_size'],
      epochs=epochs
    )

    self.__model__.summary()

    return self.__model__
