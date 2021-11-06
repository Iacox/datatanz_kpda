import io
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import xgboost as xgb
import pickle


max_review_len = 30
max_words = 35


letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя. '
print('TF version {0}'.format(tf.__version__))
print('XGBoost version {0}'.format(xgb.__version__))



def load_tokenizer(filename = 'saved_models/tokenizer.json'):
  """Функция загрузки обученного токенайзера"""
  with open(filename) as f:
    data = json.load(f)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(data)
    print('Токенайзер загружен')
    return tokenizer

def load_model():
  """Функция загрузки обученной модели TF"""
  model = tf.keras.models.load_model('saved_models/model_fio_classificaion.h5')
  print('Модель xgboost загружена')
  return model


def load_xgb():
  """Функция загрузки обученной модель градиентного бустинга"""
  bst = xgb.Booster()  # init model
  filehandler = open('saved_models/xgb.pickle.dat', 'rb')
  bst = pickle.load(filehandler)

  print('Модель классификации загружена')
  return bst




class Predictor():
  """Класс для классификации токенов"""
  def __init__(self):

    self.directory = '/files/'
    self.model = load_model()
    self.xgb   = load_xgb()
    self.tokenizer = load_tokenizer()

  def string_to_token(self, list_values):
    """Переводит строковое значение слова в токен"""
    sequences = []
    for w in list_values:
      sequences.append(np.array(self.tokenizer.texts_to_sequences([w.lower()])[0]))

    return sequences

  def token_to_tensor(self, token, max_review_len=max_review_len):
    """Переводит токен в тензор длинной 30 символов"""
    tensor = pad_sequences(token, maxlen=max_review_len)
    return tensor


  def bst_predict(self, value_string):
    """Функция классифицирует токен алгоритмом градиентного бустинга,
    вызывает методы перевода строкового значения в токен и тензор """

    value_string = self.string_to_token(value_string)
    value_string = self.token_to_tensor(value_string)
    print('Прогнозируем сущности...')
    # print(value_string, value_string[:,-3:])

    fio_class = self.xgb.predict(value_string)
    # print(fio_class)
    return fio_class



  def predict(self, value_string):
    """Функция классифицирует токен алгоритмом рекурентной нейронной сети,
        вызывает методы перевода строкового значения в токен и тензор """

    # Решено не использовать, т.к. xgboost показывал лучшие метрики на тестировании

    value_string = self.string_to_token(value_string)
    value_string = self.token_to_tensor(value_string)
    print('Прогнозируем сущности...')
    # print(value_string, value_string[:,-3:])

    fio_class = np.argmax(self.model.predict(value_string[:,-3:]), axis=1)
    # print(fio_class)
    return fio_class


