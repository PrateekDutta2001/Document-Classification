# -*- coding: utf-8 -*-
"""text-document-classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xWwZ-KAojkCirS19P1BI4u5dhgnh6j8F
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/gdrive/')
# %cd /gdrive

ls

cd/gdrive/MyDrive/Document_Classification/

ls

import numpy as np
import pandas as pd

data = pd.read_csv('data.csv')
data.head()

data.shape

data.Label.value_counts(normalize=True)

data.isnull().sum()

data.drop_duplicates(subset=['Text'], inplace=True)

data.shape

import keras
from keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer(oov_token='UNK') # oov : out of vocabulry
tokenizer.fit_on_texts(data['Text'])

# print(tokenizer.word_index)
# print(tokenizer.index_word)
# print(tokenizer.word_counts)

word_counts = len(tokenizer.word_index) + 1
print(word_counts)

"""# covert each sentence to ids"""

sequences = tokenizer.texts_to_sequences(data['Text'])

"""# padding"""

max_length = np.mean([len(seq) for seq in sequences])
print(max_length)

"""### padding : add zeros if the sentence have a words less than the max length
### truncation : remove words from sentence if it has a words above the max length.
"""

from keras.preprocessing.sequence import pad_sequences

padded_sequences = pad_sequences(sequences, padding='post', truncating='post', maxlen=400)

padded_sequences.shape

padded_sequences

"""# split the data to train and test"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(padded_sequences, data['Label'],
                                                    test_size=0.2,
                                                    random_state=123,
                                                    stratify=data['Label'],
                                                    shuffle=True)

"""# One Hot Encoding Labels"""

from keras.utils import to_categorical

y_train_encoded = to_categorical(y_train)
y_test_encoded = to_categorical(y_test)

y_train_encoded

"""# Model Building"""

def relu(x):
    return np.maximum(0, x)
relu(-10)

from keras.models import Sequential
from keras import layers

model = Sequential()
model.add(layers.Embedding(input_dim=word_counts, output_dim=300, input_length=400, mask_zero=True)) # output (عدد الكلمات في طول الفيكتور)
model.add(layers.Flatten()) # # output >>  (2127, 300) # output the average vector for each sentence
model.add(layers.BatchNormalization()) # output >>  (2127, 300)
model.add(layers.Dense(128, activation='relu')) # (300, 128)
model.add(layers.Dense(256, activation='relu')) # (128, 256) >> (2127, 256)
model.add(layers.Dense(5)) # (256, 5) >> (2127, 5)
model.add(layers.Softmax())

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

"""# Training Model"""

# model.fit(X_train, y_train_encoded, epochs=20, batch_size=128, validation_split=0.1)
model.fit(X_train, y_train_encoded, epochs=30, batch_size=128, validation_data=(X_test, y_test_encoded)) # using test data as validation data too.

model.evaluate(X_test, y_test_encoded)

predictions = model.predict(X_test).argmax(axis=1)

model.save("my_model.h5")

predictions

y_test.values

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

print(classification_report(predictions, y_test.values))

ConfusionMatrixDisplay(confusion_matrix(predictions, y_test.values),
                             display_labels=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business']).plot()

