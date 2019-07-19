# Twitter API
# http://benalexkeen.com/interacting-with-the-twitter-api-using-python/

import base64
import requests
import pandas as pd

client_key = '8AO6OU5ubyi4XO47b1C7Sjdlz'
client_secret = 'FS1usPrfPolvjLXbwGka5N8TWkOZhUsdxGmmTwuO016koesUSt'

key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
tweets = []
search_query = 'ibm'

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
# Check status code
print(auth_resp.status_code)
print(auth_resp.json().keys())

access_token = auth_resp.json()['access_token']


# Queries
search_headers = {
	'Authorization': 'Bearer {}'.format(access_token)
}

search_params = {
	'q': search_query,
	'result_type': 'recent',
	'count': 100
}

search_url = '{}1.1/search/tweets.json'.format(base_url)
search_resp = requests.get(search_url, headers=search_headers,
	params = search_params)
print(search_resp.status_code)
tweet_data = search_resp.json()
print(tweet_data)

# Print text of tweet
for tweet in tweet_data['statuses']:
	print(tweet['text'] + '\n')
	tweets.append([tweet['text'],
		tweet['favorite_count'],
		tweet['retweet_count']
		])

tweets = pd.DataFrame(tweets, columns=['text',
										'favorite_count',
										'retweet_count'])

print(tweets)
tweets.to_csv('twitter_' + search_query + '.csv', index=False, encoding='utf8')









