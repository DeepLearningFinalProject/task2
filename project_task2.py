# -*- coding: utf-8 -*-
"""Project Task2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17dgFlvka0ps39jHonQUiIZROQ3NwjNbc
"""

#%% Importing Keras(Neural network library ) for Meachine Learning

from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import Tokenizer
import pandas as pd
import keras
from sklearn import preprocessing
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D,Input

#%% Importing the dataset

from sklearn.datasets import fetch_20newsgroups

#%%fetching larger datasets

cats = ['comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware']
data_frame = fetch_20newsgroups(subset='train', shuffle=True, categories=cats)

#% Extracting sentences from dataset
sentences=data_frame.data
y=data_frame.target

#%% Importing preprocessing for changing raw feature vectors into a representation

from sklearn import preprocessing

#%%For training data and for testing data. Pad_sequences to ensure that all sequences in a list have the same length

from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences

#%% Tokenizing the data


max_features = 2000
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(data_frame.data)
X = tokenizer.texts_to_sequences(data_frame.data)
X = pad_sequences(X)


#%% to_categorical is to convert integers to binary class matrix. labelENcoder is to encode labels which are distinct

from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder

labelencoder = LabelEncoder()
integer_encoded = labelencoder.fit_transform(data_frame.target)
y = to_categorical(integer_encoded)
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.33, random_state = 42)

#%%traning and Testing the data

X_train.shape,X_test.shape,y_train.shape,y_test.shape

#%%Embedding layer


embed_dim = 128 #%Size of the vocabulary
lstm_out = 196  #% Dimension of the dense embedding

#%% Creating a model

def createmodel():
    model = Sequential()
    model.add(Embedding(max_features, embed_dim,input_length = X.shape[1]))
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(2,activation='softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
    return model

#%%

model = createmodel() #Function call to Sequential Neural Network
history1=model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=32) 


#%%Reshape the input data into a format suitable 

from keras.layers import Embedding, Flatten

#%%list all data in history

print(history1.history.keys())

#%%Plotting

import matplotlib.pyplot as plt

#%%

plt.plot(history1.history['accuracy'])
plt.plot(history1.history['val_accuracy'])
plt.title('Accuracy Plot')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

#%%

plt.plot(history1.history['loss'])
plt.plot(history1.history['val_loss'])
plt.title('Loss Plot')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

