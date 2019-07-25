import requests
import base64

client_key = '8AO6OU5ubyi4XO47b1C7Sjdlz'
client_secret = 'FS1usPrfPolvjLXbwGka5N8TWkOZhUsdxGmmTwuO016koesUSt'

key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

url = "https://api.twitter.com/1.1/followers/ids.json"
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

querystring = {"screen_name": "ibm"}

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
# Check status code
print("Status of authentication")
print(auth_resp.status_code)
print(auth_resp.json().keys())

access_token = auth_resp.json()['access_token']

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'User-Agent': "PostmanRuntime/7.15.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "857aad40-b56c-4df3-9221-d60563b3e53d,29433b93-00df-4647-bed9-7da0c6da8287",
    'Host': "api.twitter.com",
    # 'cookie': "personalization_id="v1_8iczJcVH7NfwD7U6EVC2UQ==
        # "; guest_id=v1%3A156354449360796902; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCE82jApsAToMY3NyZl9p%250AZCIlODkwMzk2MjY5MDYyNzVjMDk2MTE3OTRkZDlmN2RjNDU6B2lkIiVkZDUw%250AMzZhOTZhNDI1NGM4NGJkYjFhOWM5NGY2ZDAwNQ%253D%253D--41d0d8267c60b2d66e42d58128c56e39965c7d3d; lang=en",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


