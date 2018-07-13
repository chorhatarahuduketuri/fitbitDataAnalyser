import json
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient
import requests

secret_codes_file_path = '../secretCodes.txt'

secret_codes_file = open(secret_codes_file_path, 'r')
secret_codes_string = secret_codes_file.read()
secret_codes_file.close()
secret_codes_json = json.loads(secret_codes_string)

authorization_uri = 'https://www.fitbit.com/oauth2/authorize'
token_uri = 'https://api.fitbit.com/oauth2/token'
scopes = ['activity', 'heartrate', 'location', 'nutrition', 'profile', 'settings', 'sleep', 'social', 'weight']
token = ''

needs_authorization = input('Do you need to reauthorize? (y/n)') # for when you need to authorize
# needs_authorization = 'n' # for when you need to run it and you already have the authorization token

# Initialize client
client = MobileApplicationClient(secret_codes_json['clientId'])
fitbit = OAuth2Session(secret_codes_json['clientId'], client=client, scope=scopes)
authorization_url = "https://www.fitbit.com/oauth2/authorize"

if (needs_authorization == 'y'):
    # Grab the URL for Fitbit's authorization page.
    auth_url, state = fitbit.authorization_url(authorization_url)
    print("Visit this page in your browser: {}".format(auth_url))

    # After authenticating, Fitbit will redirect you to the URL you specified in your application settings. It contains the access token.
    callback_url = input("Paste URL you get back here: ")

    # Get the access token as a string, and update the secret codes file with it.
    access_token = callback_url.split("&")[0].split('#')[1].split('=')[1]
    secret_codes_json['accessToken'] = access_token
    state = callback_url.split('&')[3].split('=')[1]
    secret_codes_json['state'] = state
    secret_codes_file = open(secret_codes_file_path, 'w')
    secret_codes_file.write(json.dumps(secret_codes_json))
    secret_codes_file.close()

    # Now we extract the token from the URL to make use of it.
    fitbit.token_from_fragment(callback_url)
else:
    fitbit.token_from_fragment(str('https://localhost#access_token=' + secret_codes_json['accessToken'] + '&state=' + secret_codes_json['state']))

# At this point, assuming nothing blew up, we can make calls to the API as normal, for example:
response = fitbit.get('https://api.fitbit.com/1/user/-/activities/goals/daily.json')

print(type(response))
print(response.status_code)
print(response.headers)
print(response.text)