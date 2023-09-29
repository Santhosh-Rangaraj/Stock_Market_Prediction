from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import random
import string


import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
from wordcloud import WordCloud, STOPWORDS

news_api = Blueprint('news_api', __name__)

from app import newspred_collection


def predict_news(name):
	nltk.download('vader_lexicon')

	now = dt.date.today()
	now = now.strftime('%m-%d-%Y')
	yesterday = dt.date.today() - dt.timedelta(days = 1)
	yesterday = yesterday.strftime('%m-%d-%Y')

	nltk.download('punkt')
	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
	config = Config()
	config.browser_user_agent = user_agent
	config.request_timeout = 10

	company_name = name
	if company_name != '':
		print(f'Searching for and analyzing {company_name}, Please be patient, it might take a while...')

		#Extract News with Google News
		googlenews = GoogleNews(start=yesterday,end=now)
		googlenews.search(company_name)
		result = googlenews.result()
		#store the results
		df = pd.DataFrame(result)
		# print("df" , df)


	try:
		list =[] 
		for i in df.index:
			dict = {} 
			article = Article(df['link'][i],config=config) 
			try:
				article.download() 
				article.parse() 
				article.nlp() 
			except:
				pass 

			dict['Date']=df['date'][i] 
			dict['Media']=df['media'][i]
			dict['Title']=article.title
			dict['Article']=article.text
			dict['Summary']=article.summary
			dict['Key_words']=article.keywords
			list.append(dict)
		check_empty = not any(list)
		print(check_empty)
		if check_empty == False:
			news_df=pd.DataFrame(list) 
		print(news_df)
		print(news_df.Summary.to_string(index=False))

	except Exception as e:
		print("exception occurred:" + str(e))
		print('Looks like, there is some error in retrieving the data, Please try again or try with a different ticker.' )

	def percentage(part,whole):
		return 100 * float(part)/float(whole)

	positive = 0
	negative = 0
	neutral = 0
	news_list = []
	neutral_list = []
	negative_list = []
	positive_list = []

	for news in news_df['Summary']:
		news_list.append(news)
		analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
		neg = analyzer['neg']
		neu = analyzer['neu']
		pos = analyzer['pos']
		comp = analyzer['compound']

		if neg > pos:
			negative_list.append(news) 
			negative += 1 
		elif pos > neg:
			positive_list.append(news) 
			positive += 1 
		elif pos == neg:
			neutral_list.append(news) 
			neutral += 1  

	positive = percentage(positive, len(news_df)) 
	negative = percentage(negative, len(news_df))
	neutral = percentage(neutral, len(news_df))

	news_list = pd.DataFrame(news_list)
	neutral_list = pd.DataFrame(neutral_list)
	negative_list = pd.DataFrame(negative_list)
	positive_list = pd.DataFrame(positive_list)
	print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n')
	print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n')
	print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n')

	labels = ['Positive ['+str(round(positive))+'%]' , 'Neutral ['+str(round(neutral))+'%]','Negative ['+str(round(negative))+'%]']
	sizes = [positive, neutral, negative]
	colors = ['yellowgreen', 'blue','red']
	patches, texts = plt.pie(sizes,colors=colors, startangle=90)
	plt.style.use('default')
	plt.legend(labels)
	plt.title("Sentiment Analysis Result for stock= "+company_name+"" )
	plt.axis('equal')

	filename = company_name + '_' + ''.join([random.choice(string.ascii_letters+ string.digits) for n in range(5)])
	plt.savefig("../frontend/src/assets/predictions/"+filename, transparent=True, bbox_inches='tight', dpi=150)
	plt.close()
	return filename


@news_api.route("/news/<string:name>")
@jwt_required()
def get_news_pred(name):
	if True in [char.isdigit() for char in name]:
		return jsonify({"msg": "not a valid company name"}), 400
	filename = predict_news(name)
	pred_data = {
		'user_id': get_jwt_identity(),
		'company': name,
		'img_url': filename,
		'datetime': str(dt.datetime.now()),
	} 
	newspred_collection.insert_one(pred_data)

	return filename