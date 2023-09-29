import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

start = pd.to_datetime(['2017-01-01']).astype(int)[0]//10**9 
end = pd.to_datetime(['2022-08-05']).astype(int)[0]//10**9 .

company = 'AMZN'
url = 'https://query1.finance.yahoo.com/v7/finance/download/' + company + '?period1=' + str(start) + '&period2=' + str(end) + '&interval=1d&events=history'
df = pd.read_csv(url)

close = df.reset_index()['Close']

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
data = scaler.fit_transform(np.array(close).reshape(-1,1))

train_size = int(len(data)*0.75)
test_size = len(data) - train_size
print('Full Data Size: ', len(data))
print('Train Size: ', train_size)
print('Test Size: ', test_size)

train_data, test_data = data[:train_size,:], data[train_size:len(data),:] 
print('Full Data Size: ', len(data))
print('Train Size: ', len(train_data))
print('Test Size: ', len(test_data))
test_data[232:].shape

def create_dataset(dataset, time_step=1):
  datax,datay=[],[]
  for i in range(len(dataset)-time_step-1):
    a=dataset[i:(i+time_step),0]
    datax.append(a)
    datay.append(dataset[i+time_step,0])
  return np.array(datax),np.array(datay)

time_step=100
x_train,y_train=create_dataset(train_data,time_step)
x_test,y_test=create_dataset(test_data,time_step)

x_train=x_train.reshape(x_train.shape[0],x_train.shape[1],1)
x_test=x_test.reshape(x_test.shape[0],x_test.shape[1],1)

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Input
model = Sequential()
model.add(Input(shape = (100,1)))
model.add(LSTM(50,activation='relu',return_sequences=True))

model.add(LSTM(50,activation='relu', return_sequences=True))
model.add(LSTM(50,activation='relu'))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')

history = model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=100,batch_size=64,verbose=1)

s = company + '_forecast.h5'
 
model.save(s)
