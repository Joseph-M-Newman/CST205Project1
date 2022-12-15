'''
Authors: Luke Berry, Nathan Savonen, Frank Perez, Joseph Newman
Date: 12/14/2022
Course: CST 205
Title: CST 205 Final Project
Abstract: Design and develop a web-app that finds the top trends of 
		  Various social medias and place it all in one hub
'''
from flask import Flask, render_template, redirect, request, url_for
from urllib.request import Request, urlopen
import lxml
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
def IMDB():
	#Shawshank Redemption Image
	shaw = "https://flxt.tmsimg.com/assets/p15987_p_v8_ai.jpg"

	#Godfather Image
	godfather = "https://images.fandango.com/ImageRenderer/400/0/redesign/static/img/default_poster.png/0/images/masterrepository/fandango/1463/The_Godfather-2.jpg"

	#The dark knight
	batman = "https://images.pristineauction.com/158/1582578/main_1597378492-The-Dark-Knight-27x40-Movie-Poster-PristineAuction.com.jpg"

	#Lord of the rings
	LOTR = "https://ak1.ostkcdn.com/images/products/is/images/direct/ce9596d427dd2f53a3c8f9e1dba2d34e10901e8d/%22Lord-of-the-Rings-The-Return-of-the-King-%282003%29%22-Poster-Print.jpg"

	#Schindlers List
	Schin = "https://www.themoviedb.org/t/p/original/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg"

	my_site = 'https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc'

	movieList = [shaw,godfather,batman,LOTR,Schin]
	am = []


	# req = Request(
	# 	my_site,
	# 	headers={'User-Agent': 'Mozilla/5.0'}
	# )
	r = requests.get(my_site)
	resp = r.content
	soup = BeautifulSoup(resp, 'html.parser')
	all_movies = soup.find_all("h3")
	for a in all_movies:
		for b in a.find_all('a', href=True):
			am.append(b.string)
	top_5 = all_movies[:5]

	return am,movieList

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
		movie = False
		twitter = request.form["twitter"]
		reddit = request.form["reddit"]
		trending = request.form["trending"]
		movie = request.form["movie"]
		#keyword = request.form["keyword"]
		red = []
		twit = []
		trend = []
		trend2 = []
		mov = []
		mov1 = []
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
		if movie == "Movie":
			movie = True
			mov,mov1 = IMDB()

			
		return render_template("display.html", red = red[0:10], redTrue = reditt, twit=twit, twitTrue = t, trend = trend, trend2 = trend2, trendTrue = tre,movie = movie,mov = mov, mov1 = mov1)

if __name__ == "__main__":
	app.run(debug=True)