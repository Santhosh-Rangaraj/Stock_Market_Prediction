from flask import Blueprint, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import random
import string
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import datetime

forecast_api = Blueprint('forecast_api', __name__)

from app import forecast_collection

def test_model(df, company_name):
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
	x_train, y_train = np.array(x_train), np.array(y_train)
	x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
	modelname = './models/' + company_name + '.h5'
	model = load_model(modelname)

	test_data = scaled_data[training_data_len - 60: , :]
	x_test = []
	y_test = dataset[training_data_len:, :]
	for i in range(60, len(test_data)):
		x_test.append(test_data[i-60:i, 0])
		
	x_test = np.array(x_test)
	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))
	predictions = model.predict(x_test)
	predictions = scaler.inverse_transform(predictions)
	rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
	print("RMSE : " , rmse)
	# Plot the data
	train = data[:training_data_len]
	valid = data[training_data_len:]
	valid['Predictions'] = predictions
	# Visualize the data
	plt.figure(figsize=(16,6))
	plt.title('Previous 5 Years of ' + company_name + ' data')
	plt.xlabel('Days', fontsize=18)
	plt.ylabel('Close Price ', fontsize=18)
	plt.plot(train['Close'])
	plt.plot(valid[['Close', 'Predictions']])
	plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
	filename = company_name + '_' + ''.join([random.choice(string.ascii_letters+ string.digits) for n in range(5)]) + ".png"
	filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend/src/assets/forecasts/'))
	plt.savefig(filepath +'/'+ filename)
	plt.close()
	return filename

def create_dataset(dataset, time_step=1):
  datax,datay=[],[]
  for i in range(len(dataset)-time_step-1):
    a=dataset[i:(i+time_step),0]
    datax.append(a)
    datay.append(dataset[i+time_step,0])
  return np.array(datax),np.array(datay)

def forecast(company_name):
	print("company name " + company_name)
	start = pd.to_datetime(['2017-01-01']).astype(int)[0]//10**9 
	end = pd.to_datetime(['2022-06-04']).astype(int)[0]//10**9
	url = 'https://query1.finance.yahoo.com/v7/finance/download/' + company_name + '?period1=' + str(start) + '&period2=' + str(end) + '&interval=1d&events=history'
	df = pd.read_csv(url)

	filename = test_model(df, company_name)

	# # df.to_csv('infy.csv')
	# df = pd.read_csv('infy.csv')
	modelname = './models/' + company_name + '_forecast.h5'
	print("model name " + modelname )
	model = load_model(modelname)
	close = df.reset_index()['Close']

	scaler = MinMaxScaler(feature_range=(0,1))
	data = scaler.fit_transform(np.array(close).reshape(-1,1))

	train_size = int(len(data)*0.75)
	test_size = len(data) - train_size

	train_data, test_data = data[:train_size,:], data[train_size:len(data),:] 
	test_data[232:].shape
	
	time_step=100
	x_train,y_train=create_dataset(train_data,time_step)
	x_test,y_test=create_dataset(test_data,time_step)

	x_train=x_train.reshape(x_train.shape[0],x_train.shape[1],1)
	x_test=x_test.reshape(x_test.shape[0],x_test.shape[1],1)

	train_predict=model.predict(x_train)
	test_predict=model.predict(x_test)
	train_predict=scaler.inverse_transform(train_predict)
	test_predict=scaler.inverse_transform(test_predict)
	import math
	from sklearn.metrics import mean_squared_error
	print("rmse : " , math.sqrt(mean_squared_error(y_train,train_predict)))

	#split train predict for plot
	look_back=100
	trainpredictplot=np.empty_like(data)
	trainpredictplot[:, :]=np.nan
	trainpredictplot[look_back:len(train_predict)+look_back,:]=train_predict
	#shif test predict for plot
	testpredictplot=np.empty_like(data)
	testpredictplot[:, :]=np.nan
	testpredictplot[len(train_predict)+(look_back*2)+1:len(data)-1,:]=test_predict
	# plt.plot(scaler.inverse_transform(data))
	# plt.plot(trainpredictplot)
	# plt.plot(testpredictplot)
	# filename = company_name + '_' + ''.join([random.choice(string.ascii_letters+ string.digits) for n in range(5)]) + ".png"
	# filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend/src/assets/predictions/'))
	# plt.savefig(filepath +'/'+ filename, transparent=True, bbox_inches='tight', dpi=150 )
	# plt.close()

	n = len(test_data[:100:-1])
	x_input=test_data[n:].reshape(1,-1)
	# x_input=test_data[226:].reshape(1,-1)
	temp_input=list(x_input)
	temp_input=temp_input[0].tolist()
	len(temp_input)
	input = temp_input


	from statistics import mean
	from numpy import array
	lst_output=[]
	output = []
	n_steps= 100
	for day in range(30):
		x_input=np.array(temp_input[1:])
		#print("{} day input {}".format(day,x_input))
		#print(x_input)
		x_input=x_input.reshape(1,-1)
		x_input = x_input.reshape((1, n_steps, 1))
		y = mean(input)
		#print(y)
		yhat = model.predict(x_input, verbose=0)
		#print(yhat)
		#print("{} day output {}".format(day,yhat))
		input = input[1:]
		input.append(y)
		output.append(y)
		temp_input.extend(yhat[0].tolist())
		temp_input=temp_input[1:]
		lst_output.extend(yhat.tolist())


	output = np.array(output)
	out = output.reshape(30,1)
	day_new=np.arange(1,101)
	day_pred=np.arange(len(data)+1,len(data)+31)
	# plt.plot(scaler.inverse_transform(data))
	# plt.plot(day_pred,scaler.inverse_transform(out));
	filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend/src/assets/predictions/'))
	plt.title(company_name + ' data')
	plt.xlabel('30 Days', fontsize=18)
	plt.ylabel('Close Price ', fontsize=18)
	plt.plot(scaler.inverse_transform(out))
	plt.savefig(filepath +'/'+ filename, transparent=True, bbox_inches='tight', dpi=150 )
	plt.close()
	# plt.savefig('../frontend/src/assets/forecasts/'+filename, transparent=True, bbox_inches='tight', dpi=150)
	return filename

@forecast_api.route("/forecast/<name>")
@jwt_required()
def get_forecast(name):
	filename = forecast(name)
	forecast_data = {
		"user_id": get_jwt_identity(),
		"company": name,
		"img_url": filename,
		"datetime": str(datetime.datetime.now())
	}
	forecast_collection.insert_one(forecast_data)
	return filename
