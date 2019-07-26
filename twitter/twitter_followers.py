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
print("Status of authentication")
print(auth_resp.status_code)
print(auth_resp.json().keys())
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

# Lookup followers query
follower_querystring = {"user_id":"783214,6253282"}
# follower_querystring = {"user_id": user_string}




# Get list of follower ids for account = HOW TO GET ALL FOLLOWERS
# Input url = lookup_url
# headers = follower_headers
# params = follower_querystring
def get_follower_ids(account, url, head):
    # Get followers query
    querystring = {"screen_name": account,
        'count': 10}
    resp = requests.request("GET", url, 
        headers=head, 
        params=querystring)
    return resp


# Twitter API only can batch 100 followers at a time
# Batch = 100 follower IDs
def get_user_objects(follower_ids, count):
    batch_len = 100
    # num_batches = count / 100
    # batches = (follower_ids[i:i + batch_len] for i in range(0, count, batch_len))
    all_data = []
    for follower in follower_ids: #Doing this 10 times (WRONG) should be len of string
        resp = requests.request("POST", lookup_url,
            headers = follower_headers,
            params = follower_querystring) #need to change this
        follower_json = resp.json()
        all_data += follower_json
    # for batch_count, batch in enumerate(batches):
    #     # users_list = auth_api.lookup_users(user_ids=batch)
    #     # users_json = (map(lambda t: t._json, users_list))
    #     # all_data += users_json
    return all_data

# Get info from follower json object
def get_follower_info(follower_objects):
    df = []
    for obj in follower_objects:
        df.append([obj['id'],
            obj['description'],
            obj['screen_name']])
    df = pd.DataFrame(df, columns=['id', 'description', 'screen_name'])
    return df

# Get number of follower IDs and make them into a string
def num_ids(follower_ids):
    json_obj = follower_ids.json()
    list_ids = json_obj['ids']
    count = len(list_ids) #accurate count
    print(count)

    # Concatenate strings = this doesnt work bc they must be integers
    string_ids = ""
    for x in range(0, count - 1):
        string_ids += str(list_ids[x])
        string_ids += ","
    string_ids += str(list_ids[count - 1])
    print string_ids
    return string_ids


# Query for followers - need to grab all followers ==> ADD TO QUERYSTRING
user_string = ""
response = get_follower_ids("ibm", url, headers)
# print(response.text)
test = num_ids(response)

# Follower data as json object
follower_data = get_user_objects(response, 0)
# Follower data into dataframe = id, description, screen name
follower_data = get_follower_info(follower_data)
print(follower_data)










