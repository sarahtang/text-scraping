# Grabbing followers of a screen_name using Twitter API
# Getting bios and info of those followers

import requests
import base64

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


# Get followers query
querystring = {"screen_name": "ibm",
    'count': 5000}

# Lookup followers query
follower_querystring = {"user_id":"783214,6253282"}
# follower_querystring = {"user_id": user_string}







# Get all followers for querystring = HOW TO GET MORE FOLLOWERS
response = requests.request("GET", url, 
    headers=headers, 
    params=querystring)

# Query for followers - need to grab all followers ==> ADD TO QUERYSTRING
user_string = ""


# print(response.text)
# Up to 100 allowed in single request
follower_count = 0
for follower in response:
    user_string += follower + ","
    follower_count += 1

# List of all followers
print(user_string)
print(follower_count)


# Get list of follower ids for account
# Input url = lookup_url
# headers = follower_headers
# params = follower_querystring
def get_follower_ids(account, url, head, querystr):
    resp = requests.request("GET", url, 
        headers=head, 
        params=querystr)
    print("RESULT")
    print(resp.text)
    return resp


# Twitter API only can batch 100 followers at a time
# Batch = 100 follower IDs
def get_user_objects(follower_ids):
    batch_len = 100
    num_batches = len(follower_ids) / 100
    batches = (follower_ids[i:i + batch_len] for i in range(0, len(follower_ids), batch_len))
    all_data = []
    for batch_count, batch in enumerate(batches):
        sys.stdout.write("\r")
        sys.stdout.flush()
        sys.stdout.write("Fetching batch: " + str(batch_count) + "/" + str(num_batches))
        sys.stdout.flush()
        # users_list = auth_api.lookup_users(user_ids=batch)
        # users_json = (map(lambda t: t._json, users_list))
        # all_data += users_json
    return all_data






