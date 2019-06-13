#! usr/bin/env python3
from __future__ import unicode_literals
import praw #python reddit api wrapper
import pandas as pd
import datetime as dt

ai_posts = []
reddit = praw.Reddit(client_id='9Qn3lMcjYa2sSg',
					client_secret='qf6Eh1U13kBTacikeYVe74hUtzI',
					user_agent='Conversation_Hotspot')

subreddit = reddit.subreddit('all')
ai_subreddit = reddit.subreddit('Artificial')
# print(ai_subreddit.description)

# Grab most up-voted topics all-time
# Return list-like object with top-100 submission in r/artifical
top_subreddit = subreddit.top(limit=5)

# for submission in subreddit.top(limit=1):
# 	print(submission.title, submission.id)

# Get 10 "hottest" posts from ML subreddit
hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)
# for post in hot_posts:
# 	print(post.title)

# Get 10 "hottest" posts from all subreddits
all_hot_posts = reddit.subreddit('all').hot(limit=10)
# for post in all_hot_posts:
# 	print(post.title)

for post in ai_subreddit.hot(limit=100): #TODO WHAT IS HOT
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

# Export data in csv
# bypass ascii encoding error
ai_posts.to_csv('reddit_data.csv', index=False, encoding='utf8')


