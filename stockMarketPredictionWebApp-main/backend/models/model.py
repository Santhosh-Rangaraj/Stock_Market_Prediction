from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from tensorflow import keras

import matplotlib.pyplot as plt


from datetime import datetime

start = pd.to_datetime(['2017-01-01']).astype(int)[0]//10**9 
end = pd.to_datetime(['2022-08-05']).astype(int)[0]//10**9 

company = 'AMZN'
url = 'https://query1.finance.yahoo.com/v7/finance/download/' + company + '?period1=' + str(start) + '&period2=' + str(end) + '&interval=1d&events=history'
df = pd.read_csv(url)


data = df.filter(['Close'])
dataset = data.values
training_data_len = int(np.ceil( len(dataset) * .85 ))

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

train_data = scaled_data[0:int(training_data_len), :]
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])
    if i<= 61:
        print(x_train)
        print(y_train)
        print()
        
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

from keras.models import Sequential
from keras.layers import Dense, LSTM

model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape= (x_train.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=1)

model.save(company+'.h5')

