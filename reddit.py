#! usr/bin/env python3
from __future__ import unicode_literals
from datetime import datetime
import praw #python reddit api wrapper
import pandas as pd
import datetime as dt
import sys

subreddit_input = raw_input("What subreddit? ")
engaged_posts = 0

# subreddit.description
# post.title, post.id

ai_posts = [] #r/artifical
quantum_posts = [] #r/quantum, r/QuantumComputing
reddit = praw.Reddit(client_id='9Qn3lMcjYa2sSg',
					client_secret='qf6Eh1U13kBTacikeYVe74hUtzI',
					user_agent='Conversation_Hotspot')

subreddit = reddit.subreddit('all')
ai_subreddit = reddit.subreddit(subreddit_input) #edit this

# Get 10 "hottest" posts from ML subreddit
hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)


# hot, new, controversial, top, gilded, .search("SEARCH_KEYWORDS")
# Reddit request limit is 1000
# for post in ai_subreddit.search("Watson", limit=10):
for post in ai_subreddit.new(limit=1000):
	if (post.created >= 1559347200): #hardcoded for June UTC
		if (post.created < 1561939199):
			if (post.num_comments > 1):
				engaged_posts += 1
			ai_posts.append([post.title, 
						post.score, #TODO WHAT IS SCORE
						post.id,
						post.subreddit,
						post.url,
						post.num_comments,
						post.selftext,
						post.created])

ai_posts = pd.DataFrame(ai_posts, columns=['title',
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

_timestamp = ai_posts['created'].apply(get_date)
ai_posts = ai_posts.assign(timestamp = _timestamp)

# print(ai_posts)

#TODO
sum_comments = ai_posts['num_comments'].sum()
sum_posts = len(ai_posts.index)
total_conversation = sum_comments + sum_posts
print("Subreddit")
print(ai_subreddit.display_name)
print("Number of engaged posts with >= 2 comments in June")
print(engaged_posts)
print("Number of posts in June")
print(sum_posts) #number of elements in array
print("Number of comments in June")
print(sum_comments)
print("Total conversation in June")
print(total_conversation)


# Export data in csv
# bypass ascii encoding error
ai_posts.to_csv('reddit_ai_new_filterbyeng_all_june.csv', index=False, encoding='utf8')


