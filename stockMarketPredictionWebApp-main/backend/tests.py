import json
from app import app
import random
import string

app = app.test_client()

rand_str = '_' + ''.join([random.choice(string.ascii_letters+ string.digits) for n in range(5)])
username = "testn" + rand_str
email = "testn" + rand_str + "@email.com"
password = "testn" + rand_str

token = ''

def test_web_health():
	resp = app.get("/hello")
	print(resp.data)
	assert resp.data == b'hello'
	assert resp.status_code == 200

def test_signup():
	payload = json.dumps({
		"username": username,
		"email": email,
		"password": password,
	})

	resp = app.post("/user/register", headers={"Content-Type": "application/json"}, data=payload)

	print(resp.data)
	assert resp.data == b'{"msg":"user created"}\n'
	assert 200 == resp.status_code

def test_email_already_exists_for_signup():
	payload = json.dumps({
		"username": username,
		"email": email,
		"password": password,
	})

	resp = app.post("/user/register", headers={"Content-Type": "application/json"}, data=payload)

	print(resp.data)
	assert resp.data == b'{"msg":"email already exists"}\n'
	assert 409 == resp.status_code

def test_login():
	payload = json.dumps({
		"email": email,
		"password": password,
	})

	resp = app.post("/user/login", headers={"Content-Type": "application/json"}, data=payload)

	print(resp.json['access_token'])
	global token 
	token = str(resp.json['access_token'])
	assert 200 == resp.status_code
	assert True == token.startswith("eyJ")

def test_check_login_with_wrong_creds():
	payload = json.dumps({
		"email": "testn_oDM2d@email.com",
		"password": "wrong",
	})
	resp = app.post("/user/login", headers={"Content-Type": "application/json"}, data=payload)
	assert 400 == resp.status_code

def test_dashboard_feature():
	header = {
		"Authorization": "Bearer "+token,
		"Content-Type": "application/json"
	}
	resp = app.get("/user/dashboard", headers=header)
	assert 200 == resp.status_code

def test_dashboard_feature_without_authToken():
	header = {
		"Content-Type": "application/json"
	}
	resp = app.get("/user/dashboard", headers=header)
	assert resp.data == b'{"msg":"Missing Authorization Header"}\n'
	assert 401 == resp.status_code

def test_forecast_feature():
	header = {
		"Authorization": "Bearer "+token,
		"Content-Type": "application/json"
	}
	resp = app.get("/forecast/INFY.NS", headers=header)
	assert True == str(resp.data.decode()).startswith("INFY")
	assert 200 == resp.status_code

def test_forecast_without_token():
	header = {
		"Content-Type": "application/json"
	}
	resp = app.get("/forecast/INFY.NS", headers=header)
	print(resp.data)
	assert resp.data == b'{"msg":"Missing Authorization Header"}\n'
	assert 401 == resp.status_code

def test_forecast_without_companyname():
	header = {
		"Authorization": "Bearer "+token,
		"Content-Type": "application/json"
	}
	resp = app.get("/forecast", headers=header)
	assert 404 == resp.status_code

def test_news_analysis():
	header = {
		"Authorization": "Bearer "+token,
		"Content-Type": "application/json"
	}
	res = app.get("/news/mahindra", headers=header)
	assert 200 == res.status_code

def test_news_analysis_with_wrong_name():
	header = {
		"Authorization": "Bearer "+token,
		"Content-Type": "application/json"
	}
	res = app.get("/news/mahindra123", headers=header)
	assert 400 == res.status_code

def test_tweets_analysis():
	header = {
		"Authorization": "Bearer "+token,
		"Content-Type": "application/json"
	}
	res = app.get("/tweets/mahindra", headers=header)
	assert 200 == res.status_code

def test_tweets_analysis_with_wrong_name():
	header = {
		"Authorization": "Bearer "+token,
		"Content-Type": "application/json"
	}
	res = app.get("/tweets/mahindra123", headers=header)
	assert 400 == res.status_code