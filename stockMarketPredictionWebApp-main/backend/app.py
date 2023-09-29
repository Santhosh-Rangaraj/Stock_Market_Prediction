
import datetime
from bson import UuidRepresentation, json_util
from flask import Flask, jsonify, request
from flask_cors import CORS
from numpy import identity
from pymongo import MongoClient
import urllib
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
# from passlib.hash import sha256_crypt

# mongodb+srv://tom:<password>@clusterwebapp.6pdxi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority

app = Flask(__name__)
CORS(app)

mongo_uri = "mongodb+srv://tom:" + urllib.parse.quote_plus("TomMongo456$%") + "^@clusterwebapp.6pdxi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(mongo_uri, UuidRepresentation='standard')
db = client["StockMarketPred"]
user_collection = db["user"]
newspred_collection = db["newsPred"]
tweetpred_collection = db["tweetspred"]
pref_collection = db["prefereces"]
forecast_collection = db["forecast"]
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'hkcubwebwe'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

from tweetsApi import tweets_api
from newsApi import news_api
from forecastApi import forecast_api
app.register_blueprint(tweets_api)
app.register_blueprint(news_api)
app.register_blueprint(forecast_api)

@app.route('/hello')
def hello():
    return 'hello'

@app.route("/user/profile")
@jwt_required()
def profile():
    currentUser = get_jwt_identity()
    print(currentUser)
    user = user_collection.find_one({"id" : uuid.UUID(currentUser)})
    print(user)
    if user:
        print("Reach")
        print(user["username"])
        return jsonify({'profile': user["username"]})
    else:
        return jsonify({'msg': 'not logged in'})

@app.route("/user/add-pref", methods=["post"])
@jwt_required()
def add_preferences():
    companies = request.get_json()
    print(companies['names'])
    user_pref = {
        'user_id': get_jwt_identity(),
        'companies': 'hello'
    }
    pref_collection.insert_one(user_pref)
    return jsonify({'msg': 'success'})

@app.route("/user/preference")
def get_stock_prices():
    companies = ["AAPL", "MSFT", "INFY"]
    all_symbols = " ".join(companies)

    info = Ticker(all_symbols)
    dic = info.price
    details = {}
    for ticker in companies:
        ticker = str(ticker)
        price = dic[ticker]['regularMarketPrice']
        details[ticker] = price
    return jsonify({"details" : details})

@app.route("/user/login", methods=["post"])
def login():
    login_details = request.get_json()
    user = user_collection.find_one({'email': login_details["email"]})
    if user:
        if check_password_hash(user["password"], login_details["password"]):
            token = create_access_token(identity=user["id"])
            return jsonify(access_token=token)
    return jsonify({'msg': 'Username or password Incorrect'}), 400


@app.route("/user/register", methods=["post"])
def register():
    new_user = request.get_json()
    new_user["password"] = generate_password_hash(new_user["password"])
    id =  uuid.uuid4()
    new_user["id"] = id
    doc = user_collection.find_one({"email": new_user["email"]})
    if not doc:
        user_collection.insert_one(new_user)
        return jsonify({"msg": "user created"}), 200
    else:
        return jsonify({"msg": "email already exists"}), 409 

@app.route("/user/dashboard", methods=["get"])
@jwt_required()
def get_dashboard():
    user = get_jwt_identity()
    data = []
    tweets_data = tweetpred_collection.find({"user_id": user}, {"_id": 0, "company": 1, "img_url": 1, "datetime": 1})
    tweets_data = json.loads(json_util.dumps(tweets_data))
    data.extend(tweets_data)
    news_data = newspred_collection.find({"user_id": user}, {"_id": 0, "company": 1, "img_url": 1, "datetime": 1})
    news_data = json.loads(json_util.dumps(news_data))
    data.extend(news_data)
    forecast_data = forecast_collection.find({"user_id": user}, {"_id": 0, "company": 1, "img_url": 1, "datetime": 1})
    forecast_data = json.loads(json_util.dumps(forecast_data))
    data.extend(forecast_data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)