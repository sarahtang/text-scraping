# Grabbing followers of a screen_name using Twitter API
# Getting bios and info of those followers
# 75,000 followers every 15 minutes

import requests
import base64
import json
import pandas as pd
import time
import pickle
import ast

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


# Get rate limit
def get_rate_limit():
    rate_query = {"resources":"followers,users"}
    rate_response = requests.request("GET", 
                                    rate_url,
                                    headers=rate_headers,
                                    params = rate_query)
    rate_response_json = rate_response.json()
    # print(rate_response_json)
    follower_id_limit = rate_response_json['resources']['followers']['/followers/ids']
    print(follower_id_limit)
    follower_id_remaining = follower_id_limit['remaining']
    follower_id_reset = follower_id_limit['reset']
    # print(follower_id_remaining)
    return follower_id_remaining



# Input url = lookup_url
# headers = follower_headers
# Twitter API call to get list of follower ids for an account
def get_follower_ids(account, head, cursor):
    # Get followers query
    querystring = {"screen_name": account,
        'count': 5000, #change count here, max 5000
        'cursor': cursor}
    resp = requests.request("GET", 
        "https://api.twitter.com/1.1/followers/ids.json", 
        headers=head, 
        params=querystring)
    return resp


# Twitter API call to get user objects
# ID info for list of followers
def get_user_objects(follower_ids, count = 0):
    # batch_len = 10
    all_data = []
    for f_id in follower_ids: #how many follower IDs
        count += 1
        print('How many follower ids:')
        print(count)
        foll_query = {} #dictionary
        foll_query['user_id'] = f_id
        resp = requests.request("POST", lookup_url,
            headers = follower_headers,
            params = foll_query)
        follower_json = resp.json()
        all_data += follower_json
    print("Total count of follower objects:")
    print(count)
    return all_data

# Get info from follower json object [LIST]
# WRONG
# follower_object is a single json object with follower info // dict
def get_follower_info_list(follower_object):
    df = []
    # print(follower_object)
    # print(type(follower_object))

    # Convert to dictionary
    d = {}
    for each in follower_object:
    	# each.json() #does this change anything? --> maybe now i can make better calls?

        print("one follower object")
        print(each)
        print(type(each)) #dictionary type, unicode strings

        #TEST
        # each = json.dumps(each) #removing the 'u', data dump
        # print(each)
        # print(type(each)) #str

        d['name'] = each['name']
        d['screen_name'] = each['screen_name']
        d['description'] = each['description']
        # d['verified'] = each['verified']
        # d['followers_count'] = each['followers_count']
        # d['statuses_count'] = each['statuses_count']
        # d['url'] = each['url']
        # d['created_at'] = each['created_at']
        d['mentions_ibm'] = 0
        d['blank_bio'] = 0
        if "ibm" in d['description']:
            d['mentions_ibm'] = 1 # 1 = mentions IBM
        if "IBM" in d['description']:
            d['mentions_ibm'] = 1
        if not d['description']: # 1 = blank bio
            d['blank_bio'] = 1

        df.append([d['name'],
                d['screen_name'],
                d['description'],
                # d['verified'],
                # d['followers_count'],
                # d['statuses_count'],
                # d['url'],
                # d['created_at'],
                d['mentions_ibm'],
                d['blank_bio']])

    # df = pd.DataFrame(d, index=['i', ])
    
    df = pd.DataFrame(df, columns=['name',
                                    'screen_name',
                                    'description',
                                    # 'verified',
                                    # 'followers_count',
                                    # 'statuses_count',
                                    # 'url',
                                    # 'created_at',
                                    'mentions_ibm',
                                    'blank_bio'])

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

# Can grab all followers
# Gets all followers at a rate of 150 ids per 15 mins
# Initialize rate limit, 150 ids per round
def get_all_follower_ids(df, cursor, rate_limit, account, h): # Made this a function
    minute = 0
    while (cursor != 0):
        if (rate_limit != 0):
            response = get_follower_ids(account, h, cursor)
            response_json = response.json() # get list of followers per batch
            for ids in response_json['ids']:
                df.append(ids)
            cursor = response_json['next_cursor']
            # print(response_json)
        else:
            print("This prints once a minute. Round:")
            print(minute)
            time.sleep(60)
            minute += 1
        rate_limit = get_rate_limit() # update rate limit
        print(rate_limit)
    return df


# SPLIT DF INTO CHUNKS
# Yield successive n-sized chunks of l ===============================
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def split_into_chunks(list_follower_ids, size_of_chunk = 5000):
    list_chunks = list(chunks(list_follower_ids, size_of_chunk))
    print(list_chunks)
    num = 1
    for chunk in list_chunks:
        print(len(chunk))
        name = account + '_chunk' + str(num) + '.txt'
        with open(name, "wb") as fp:
            pickle.dump(chunk, fp)
        num += 1
    return list_chunks


# Get user objects for list of followers ================================
# Turn each chunk into CSV of follower info
def chunk_to_follower_csv(account, chunk_name):
    with open(chunk_name + '.txt', "rb") as fp:
        loaded = pickle.load(fp)
    # print(loaded)
    follower_data = get_user_objects(loaded, 0) # list
    print(type(follower_data))
    # print("FOLLOWER DATA")

    df_chunk = []
    df_chunk = get_follower_info_list(follower_data) # ERROR
    print(df_chunk)
    df_chunk.to_csv('twitter_followers_' + chunk_name + 'TEST.csv', index=False, encoding='utf8')
    # to_excel('.xls')
    return df_chunk






# FUNCTION CALLS ===============================================================================
# ==============================================================================================

df_ids = [] # Dataframe of ALL follower IDs
initial_rate_limit = get_rate_limit()
account = "IBMWatson" #ibm ==================================================== Change Account Handle

# # Call to get all followerids
# get_all_follower_ids(df_ids, -1, initial_rate_limit, account, headers) # Get follower objects

# df_ids = pd.DataFrame(df_ids, columns = ['follower_id']) #This has correct number and IDs ==> use this in get_user_objects
# print('number of dataframe ids')
# print(df_ids)

# # List of all ids
# list_follower_ids = df_ids['follower_id'].tolist() # ===================

# # Split  df into chunks
# split_into_chunks(list_follower_ids, 5)

# Chunks to csv
chunk_name = "IBMWatson_chunk19"
chunk_to_follower_csv(account, chunk_name) #ERROR IN HERE







