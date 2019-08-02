# Grabbing followers of a screen_name using Twitter API
# Getting bios and info of those followers

import requests
import base64
import json
import pandas as pd

client_key = '8AO6OU5ubyi4XO47b1C7Sjdlz'
client_secret = 'FS1usPrfPolvjLXbwGka5N8TWkOZhUsdxGmmTwuO016koesUSt'

# Encode headers
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

# URLs for API calls
url = "https://api.twitter.com/1.1/followers/ids.json"
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
lookup_url = "https://api.twitter.com/1.1/users/lookup.json"
rate_url = 'https://api.twitter.com/1.1/application/rate_limit_status.json'

# AUTHENTICATION
# Authentication header
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

# Authentication query
auth_data = {
    'grant_type': 'client_credentials'
}

# Check status code for authentication
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
# print("Status of authentication")
# print(auth_resp.status_code)
# print(auth_resp.json().keys())
access_token = auth_resp.json()['access_token']


# SET UP QUERIES AND HEADERS
# Header to get followers
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'User-Agent': "PostmanRuntime/7.15.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "857aad40-b56c-4df3-9221-d60563b3e53d,29433b93-00df-4647-bed9-7da0c6da8287",
    'Host': "api.twitter.com",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }


# Header to lookup followers
follower_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'User-Agent': "PostmanRuntime/7.15.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "a3ca97e9-1323-4fd3-8f00-310ad26b9fb1,037effc7-92bf-495f-8c20-636d6e911527",
    'Host': "api.twitter.com",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

# Rate limit header
rate_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'User-Agent': "PostmanRuntime/7.15.2",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "50e86b13-f069-452f-b56e-5da809670c38,60acac1f-6bba-40f6-8a8b-9bbf1f005959",
    'Host': "api.twitter.com",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }




# GET RATE LIMIT
rate_query = {"resources":"followers,users"}
rate_response = requests.request("GET", 
                                rate_url,
                                headers=rate_headers,
                                params = rate_query)
print(rate_response.text)




# Get list of follower ids for account = HOW TO GET ALL FOLLOWERS
# Input url = lookup_url
# headers = follower_headers
def get_follower_ids(account, head, cursor):
    # Get followers query
    querystring = {"screen_name": account,
        'count': 10, #change count here, max 1000
        'cursor': cursor}
    resp = requests.request("GET", 
        "https://api.twitter.com/1.1/followers/ids.json", 
        headers=head, 
        params=querystring)
    return resp


# Twitter API only can batch 100 followers at a time
# Batch = 100 follower IDs
def get_user_objects(follower_ids, count):
    batch_len = 10
    # num_batches = count / 100
    # batches = (follower_ids[i:i + batch_len] for i in range(0, count, batch_len))
    all_data = []
    for f_id in follower_ids:
        foll_query = {} #dictionary
        foll_query['user_id'] = f_id
        resp = requests.request("POST", lookup_url,
            headers = follower_headers,
            params = foll_query)
        follower_json = resp.json()
        all_data += follower_json
    return all_data

# Get info from follower json object [LIST]
def get_follower_info_list(follower_objects):
    df = []
    for obj in follower_objects:
        mentions_ibm = '0'
        if "ibm" in obj['description']:
            mentions_ibm = '1'
        if "IBM" in obj['description']:
            mentions_ibm = '1'
        df.append([obj['id'],
            obj['screen_name'],
            obj['name'],
            obj['description'],
            obj['verified'],
            obj['followers_count'],
            obj['statuses_count'],
            obj['url'],
            obj['created_at'],
            mentions_ibm])
    df = pd.DataFrame(df, columns=['id',
                                    'screen_name',
                                    'name',
                                    'description',
                                    'verified',
                                    'followers_count',
                                    'statuses_count',
                                    'url',
                                    'created_at',
                                    'mentions_ibm'])
    return df


# Get number of follower IDs and make them into a string
# INFO for follower querystring
def num_ids(follower_ids):
    json_obj = follower_ids.json()
    list_ids = json_obj['ids']
    count = len(list_ids) #accurate count
    print("Number of followers: ")
    print(count)

    string_ids = ""
    for x in range(0, count - 1):
        string_ids += str(list_ids[x])
        string_ids += ","
    string_ids += str(list_ids[count - 1])
    print(string_ids)
    return string_ids


# Query for followers - need to grab all followers
account = "ibm"
cursor = -1
df_ids = [] # Dataframe of follower IDs
while (cursor != 0):
    response = get_follower_ids(account, headers, cursor)
    response_json = response.json() #get list of followers
    for ids in response_json['ids']:
        df_ids.append(ids)
    cursor = response_json['next_cursor']
    print(response_json)
    if df_ids.count > 100:
        break

df_ids = pd.DataFrame(df_ids, columns = ['follower_id'])
print(df_ids) #Currently getting 1000 ids



# Un comment this part out after dealing with pagination ===================>

# List of all ids
# list_follower_ids = response_json['ids'] #need to make sure this continues to work =========>
# print(list_follower_ids)

# Get user objects for list of followers
# follower_data = get_user_objects(list_follower_ids, 0)
# print(follower_data) # print JSON object

# df = []
# df = get_follower_info_list(follower_data)
# print(df)

# df.to_csv('twitter_followers_' + account + '.csv', index=False, encoding='utf8')











