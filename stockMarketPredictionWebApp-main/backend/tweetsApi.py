from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import re
from wordcloud import WordCloud, STOPWORDS
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
import nltk
import random
import string
import datetime

tweets_api = Blueprint('tweets_api', __name__)

from app import tweetpred_collection

nltk.download('vader_lexicon')


def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text) 
    text = re.sub('#', '', text) 
    text = re.sub('RT[\s]+', '', text) 
    text = re.sub('https?:\/\/\S+', '', text) 
    return text

def percentage(part,whole):
    return 100 * float(part)/float(whole)

def predict_tweets_sentiment(name):
	query = name
	noOfTweet = 100
	noOfDays = 3

	tweets_list = []
	now = dt.date.today()
	now = now.strftime('%Y-%m-%d')
	yesterday = dt.date.today() - dt.timedelta(days = int(noOfDays))
	yesterday = yesterday.strftime('%Y-%m-%d')
	for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query + ' lang:en since:' +  yesterday + ' until:' + now + ' -filter:links -filter:replies').get_items()):
		if i > int(noOfTweet):
			break
		tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.username])

	df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
	df["Text"] = df["Text"].apply(cleanTxt)

	positive = 0
	negative = 0
	neutral = 0
	tweet_list1 = []
	neutral_list = []
	negative_list = []
	positive_list = []

	for tweet in df['Text']:
		tweet_list1.append(tweet)
		analyzer = SentimentIntensityAnalyzer().polarity_scores(tweet)
		neg = analyzer['neg']
		neu = analyzer['neu']
		pos = analyzer['pos']
		comp = analyzer['compound']

		if neg > pos:
			negative_list.append(tweet) 
			negative += 1 
		elif pos > neg:
			positive_list.append(tweet) 
			positive += 1 
		elif pos == neg:
			neutral_list.append(tweet) 
			neutral += 1  

	positive = percentage(positive, len(df)) 
	negative = percentage(negative, len(df))
	neutral = percentage(neutral, len(df))

	tweet_list1 = pd.DataFrame(tweet_list1)
	neutral_list = pd.DataFrame(neutral_list)
	negative_list = pd.DataFrame(negative_list)
	positive_list = pd.DataFrame(positive_list)

	labels = ['Positive ['+str(round(positive))+'%]' , 'Neutral ['+str(round(neutral))+'%]','Negative ['+str(round(negative))+'%]']
	sizes = [positive, neutral, negative]
	colors = ['green', 'blue','red']
	patches, texts = plt.pie(sizes,colors=colors, startangle=90)
	plt.style.use('default')
	plt.legend(labels)
	plt.title("Twitter Sentiment Analysis Result for keyword= "+query+"" )
	plt.axis('equal')

	filename = name + '_' + ''.join([random.choice(string.ascii_letters+ string.digits) for n in range(5)])
	plt.savefig("../frontend/src/assets/predictions/"+filename, transparent=True, bbox_inches='tight', dpi=150)
	return filename


@tweets_api.route("/tweets/<string:name>")
@jwt_required()
def get_tweets_pred(name):
	if True in [char.isdigit() for char in name]:
		return jsonify({"msg": "not a valid company name"}), 400

	filename = predict_tweets_sentiment(name)
	tweets_data = {
		'user_id': get_jwt_identity(),
		'company': name,
		'img_url': filename,
		'datetime': str(datetime.datetime.now())
	}
	tweetpred_collection.insert_one(tweets_data);
	return filename