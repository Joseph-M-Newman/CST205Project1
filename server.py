from flask import Flask, render_template
import flask
import praw
import tweepy
from pprint import pprint
import requests #required for ABC news trending
from bs4 import BeautifulSoup #required for ABC news trending

reddit = praw.Reddit(
	client_id="5DARDMSn1eAPkxNksqwILQ",
	client_secret="3Oig8HDiISuXjX3g47oQMArtmi4pAg",
	password="Projectcsumb",
	user_agent="script for CSUMB project",
	username="Csumbproject",
)
reddit.read_only = False
# documantation of PRAW is located https://praw.readthedocs.io/en/stable/getting_started/quick_start.html
# this holds the functions of what reddit can pull and how to use the tokens provided;
def redditApiSearch(reddit, word):
	for submission in reddit.front.hot():
		print(submission.title)

#test functionality for apiSearch returns tokens; convert tokens
redditApiSearch(reddit, "tempword")
app = Flask(__name__,  static_folder="public", static_url_path="")

@app.route('/')
def default():
	return flask.render_template("index.html") 


if __name__ == "__main__":
    app.run(debug=True)

#twitter
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKvrjQEAAAAAC7rhBPngaUoWZtiE2Po8AI7K0bM%3De9ddHzssMxizr1AxPW4EBmqwKldD8rGDLHnhtXVNXuNd67vcCU"

consumer_key = "llUeaLvBSqztrsxAMisU5YFTc"
consumer_secret = "hgpOJwGOQxFSxjIwtq5zTMSNnstlTcWfP0CFIsUWJxy26mpphi"

access_token = "1593728029452165120-jd6awx3dvx6L6HORTkq99PF1yqsTcS"
access_token_secret = "57Emarc4sTbb2yWvGZKumjhWZ3S7PAn5nSs4vTPljYFs1"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

@app.route('/twitter_trends')
def trends():
    api = tweepy.API(auth)
    #america trends: 23424977
    loc = 1
    locname = 'Earth'
    #allow user to enter a country, find the corresponding country IDs
    trends = api.get_place_trends(loc)[0]['trends']

    #pprint(trends[0]['name'])

    print('Top 5 Trending in '+ locname +': \n', '1. ' + trends[0]['name'] + '\n',
    '2. ' + trends[1]['name'] + '\n', '3. ' + trends[2]['name'] + '\n', '4. ' + trends[3]['name'] + '\n', '5. ' + trends[4]['name'] + '\n')

    
    return flask.render_template("index.html")

@app.route('/abcnews_trends')
def abcnews():
	webpage_response = requests.get('https://abcnews.go.com/')
	webpage = webpage_response.content
	abc = BeautifulSoup(webpage, "html.parser")

	title = []
	for title in abc.find_all("h2"):
		title.append(title["h2"])

	href = []
	for link in abc.find_all('a', href=True):
		href.append(link['href'])

	#Titles 14-18
	story1title = title[14]
	story2title = title[15]
	story3title = title[16]
	story3title = title[17]
	story4title = title[18]

	#Links 16-20
	story1link = href[16]
	story2link = href[17]
	story3link = href[18]
	story4link = href[19]
	story5link = href[20]
