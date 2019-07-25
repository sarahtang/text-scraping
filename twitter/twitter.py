import json
import tweepy
from twython import Twython
import pandas as pd
from tweepy import OAuthHandler
from tweepy import Stream
import requests
from tweepy.streaming import StreamListener


# Twitter credentials
twitter_credentials = dict()
twitter_credentials['CONSUMER_KEY'] = '8AO6OU5ubyi4XO47b1C7Sjdlz'
twitter_credentials['CONSUMER_SECRET'] = 'FS1usPrfPolvjLXbwGka5N8TWkOZhUsdxGmmTwuO016koesUSt'
twitter_credentials['ACCESS_KEY'] = '1151573806680592384-OUFeUtpsRFZM6jQxl1AG99NEjlY0Kt'
twitter_credentials['ACCESS_SECRET'] = 'KKHmkHkDGVaDof8XK4fKKI52DmNl4vZlaXnx85WRfd4Lr'

# Json object
with open('twitter_credentials.json', 'w') as secret_info:
	json.dump(twitter_credentials, secret_info, indent=4, sort_keys=True)

# Load Twitter API credentials
with open('twitter_credentials.json') as cred_data:
	info = json.load(cred_data)
	consumer_key = info['CONSUMER_KEY']
	consumer_secret = info['CONSUMER_SECRET']
	access_key = info['ACCESS_KEY']
	access_secret = info['ACCESS_SECRET']


with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# Create our query
query = {'q': 'learn python',
        'result_type': 'popular',
        'count': 10,
        'lang': 'en',
        }

dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])

# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)
df.sort_values(by='favorite_count', inplace=True, ascending=False)
df.head(5)


print(df)
df.to_csv('twitter.csv', index=False, encoding='utf8')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


request = requests.get('https://api.twitter.com/1.1/search/tweets.json')
print(request)




# auth2 = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# api = tweepy.API(auth2)
# for tweet in tweepy.Cursor(api.search, q='ibm').items(10):
#     print(tweet.text)


# # Streaming tweets
# # This is a basic listener that just prints received tweets to stdout.
# class StdOutListener(StreamListener):

#     def on_data(self, data):
#         print data
#         return True

#     def on_error(self, status):
#         print status

# if __name__ == '__main__':

#     #Twitter authentification + connection to Twitter Streaming API
#     l = StdOutListener()
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     stream = Stream(auth, l)

#     #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
#     stream.filter(track=['python', 'javascript', 'ruby'])


