# Twitter API credentials
consumer_key = "pIXd6jzVXnsVvIzDSkRn7EJhZ"
consumer_secret = "4fBrwRdUasmgePgBWAN4VEXxNQ3DDxKZL77vLSnZ6MWm2msxfR"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPSgugEAAAAAKHh0URHPxbIaq4suuZrBiiW8OhM%3DtthPaJUgpSi0RPpE7tMo43Su8u7RmGFJck9RhTXcTmu7FkU9UA"
access_token = "1760515708310421504-AbYnEHUA0dh50h91d1lq50t2z9LHQl"
access_token_secret = "V2BpDFSvi7VR5gmxQVufimJwmocIwzJCdj2v55ft5wbXB"

from requests_oauthlib import OAuth1Session
import os
import json

# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
payload = {"text": "Hello world!"}

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )
# Make the request
url = "https://api.twitter.com/1.1/statuses/update.json"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

response = oauth.post(url, params=payload)

# Print data from the response
print(response.text)

# Check for errors

if response.status_code == 200:
    print("Success!")
else:

    print("An error occurred: %s" % response.text)
