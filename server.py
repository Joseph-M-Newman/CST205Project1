from flask import Flask, render_template
import flask
import praw


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