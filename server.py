from flask import Flask, render_template, redirect, request, url_for
import flask
import praw
import tweepy
from pprint import pprint
import requests #required for ABC news trending
from bs4 import BeautifulSoup #required for ABC news trending

# documantation of PRAW is located https://praw.readthedocs.io/en/stable/getting_started/quick_start.html
# this holds the functions of what reddit can pull and how to use the tokens provided;

#Reddit function
def redditApiSearch(reddit, word):
	s = []
	for submission in reddit.front.hot():
		s.append(submission.title)
	return s

#End Reddit

# Begining abc Trends
def getTrending():
	msg1 = []
	msg2 = []
	webpage_response = requests.get('https://abcnews.go.com/')
	webpage = webpage_response.content
	abc = BeautifulSoup(webpage, "html.parser")

	title = []
	for story in abc.find_all("h2"):
		title.append(story.string)

	links = []
	for link in abc.find_all('a', href=True):
		links.append(link.string)

	for i in range(14,19):
		msg1.append(title[i])
	for i in range(16,20):
		msg2.append(links[i])

	#Titles 14-18
	story1title = title[14]
	story2title = title[15]
	story3title = title[16]
	story4title = title[17]
	story5title = title[18]

	#Links 16-20
	story1link = links[16]
	story2link = links[17]
	story3link = links[18]
	story4link = links[19]
	story5link = links[20]

	
	return msg1, msg2

#End abc trends

#Twitter
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKvrjQEAAAAAC7rhBPngaUoWZtiE2Po8AI7K0bM%3De9ddHzssMxizr1AxPW4EBmqwKldD8rGDLHnhtXVNXuNd67vcCU"

consumer_key = "llUeaLvBSqztrsxAMisU5YFTc"
consumer_secret = "hgpOJwGOQxFSxjIwtq5zTMSNnstlTcWfP0CFIsUWJxy26mpphi"

access_token = "1593728029452165120-jd6awx3dvx6L6HORTkq99PF1yqsTcS"
access_token_secret = "57Emarc4sTbb2yWvGZKumjhWZ3S7PAn5nSs4vTPljYFs1"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def getTwitter():
	msg = []
	api = tweepy.API(auth)
	#america trends: 23424977
	loc = 1
	locname = 'Earth'
	#allow user to enter a country, find the corresponding country IDs
	trends = api.get_place_trends(loc)[0]['trends']
	for i in range(5):
		msg.append(trends[i]['name'])
	return msg

# End Twitter

app = Flask(__name__,  static_folder="public", static_url_path="")

@app.route('/', methods=["GET", "POST"])
def default():
	return flask.render_template("index.html") 

@app.route('/display', methods=["GET", "POST"])
def display():
	if request.method == "POST":
		t = False
		reditt = False
		tre = False
		twitter = request.form["twitter"]
		reddit = request.form["reddit"]
		trending = request.form["trending"]
		#keyword = request.form["keyword"]
		red = []
		twit = []
		trend = []
		if twitter == "Twitter":
			t = True
			twit = getTwitter()
		if reddit == "Reddit":
			r = praw.Reddit(
				client_id="5DARDMSn1eAPkxNksqwILQ",
				client_secret="3Oig8HDiISuXjX3g47oQMArtmi4pAg",
				password="Projectcsumb",
				user_agent="script for CSUMB project",
				username="Csumbproject",
			)
			r.read_only = False
			red = redditApiSearch(r, "")
			reditt = True
		if trending == "Trending":
			tre = True
			trend, trend2 = getTrending()
			print(trend)
		return render_template("display.html", red = red[0:10], redTrue = reditt, twit=twit, twitTrue = t, trend = trend, trend2 = trend2, trendTrue = tre)

if __name__ == "__main__":
	app.run(debug=True)