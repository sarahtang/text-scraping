import json
import tweepy

# Twitter credentials
twitter_credentials = dict()
twitter_credentials['CONSUMER_KEY'] = '8AO6OU5ubyi4XO47b1C7Sjdlz'
twitter_credentials['CONSUMER_SECRET'] = 'FS1usPrfPolvjLXbwGka5N8TWkOZhUsdxGmmTwuO016koesUSt'
twitter_credentials['ACCESS_KEY'] = '1151573806680592384-OUFeUtpsRFZM6jQxl1AG99NEjlY0Kt'
twitter_credentials['ACCESS_SECRET'] = 'KKHmkHkDGVaDof8XK4fKKI52DmNl4vZlaXnx85WRfd4Lr'

with open('twitter_credentials.json', 'w') as secret_info:
	json.dump(twitter_credentials, secret_info, indent=4, sort_keys=True)


# Load Twitter API credentials
with open('twitter_credentials.json') as cred_data:
	info = json.load(cred_data)
	consumer_key = info['CONSUMER_KEY']
	consumer_secret = info['CONSUMER_SECRET']
	access_key = info['ACCESS_KEY']
	access_secret = info['ACCESS_SECRET']