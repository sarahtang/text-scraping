#! usr/bin/env python3
from __future__ import unicode_literals
from datetime import datetime
import praw #python reddit api wrapper
import pandas as pd
import datetime as dt
import sys
import prawcore
import time
import cgi #pass from html

# Values from html
form = cgi.FieldStorage()
searchterm =  form.getvalue('subreddit_box')


reddit = praw.Reddit(client_id='9Qn3lMcjYa2sSg',
					client_secret='qf6Eh1U13kBTacikeYVe74hUtzI',
					user_agent='Conversation_Hotspot')
unix_time = int(time.time())
# subreddit_input = raw_input("What subreddit? ")
# subreddit = reddit.subreddit(subreddit_input)
# subreddit = searchterm
engaged_posts = 0
posts = []


# Catch error if subreddit doesn't exist
def sub_exists(sub):
	exists = True
	try:
	    reddit.subreddits.search_by_name(sub, exact=True)
	except prawcore.exceptions.NotFound:
	    exists = False
	return exists

if not sub_exists(subreddit_input):
	print ("Not a valid subreddit. Try again.")
	sys.exit()


# Term frequency for posts within month
term_frequency = {"technology": 0, "engineer": 0, "watson": 0, "ibm": 0} #dictionary


# hot, new, controversial, top, gilded, .search("SEARCH_KEYWORDS")
# Reddit request limit is 1000
# for post in ai_subreddit.search("Watson", limit=10):
for post in subreddit.new(limit=1000):
	if (post.created >= unix_time - 2678400): # 31 days
		if (post.created <= unix_time):
			if (post.num_comments > 1):
				engaged_posts += 1

			for key in term_frequency:
				if key in post.title.lower():
					term_frequency[key] += 1

			posts.append([post.title, 
						post.score, #TODO WHAT IS SCORE
						post.id,
						post.subreddit,
						post.url,
						post.num_comments,
						post.selftext,
						post.created])

posts = pd.DataFrame(posts, columns=['title',
									'score',
									'id',
									'subreddit',
									'url',
									'num_comments',
									'body',
									'created'])

# Fixing format of date column
def get_date(created):
	return dt.datetime.fromtimestamp(created)

_timestamp = posts['created'].apply(get_date)
posts = posts.assign(timestamp = _timestamp)


#Output
sum_comments = posts['num_comments'].sum()
sum_posts = len(posts.index)
total_conversation = sum_comments + sum_posts
print("Subreddit: " + subreddit.display_name)
print("Number of engaged posts with >= 2 comments in last month")
print(engaged_posts)
print("Number of posts in last month")
print(sum_posts) #number of elements in array
print("Number of comments in last month")
print(sum_comments)
print("Total conversation in last month")
print(total_conversation)
print("Term frequency in post title")

for key, val in term_frequency.items():
	print("%s: %s" % (key, val))


# Export data in csv 
# bypass ascii encoding error
posts.to_csv('reddit_' + subreddit_input + '.csv', index=False, encoding='utf8')


