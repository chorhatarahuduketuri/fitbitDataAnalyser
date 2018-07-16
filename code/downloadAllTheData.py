import json
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient
from datetime import datetime, timedelta
import time


# Function to make date strings and add them to a list
def walk_days(start_date, end_date, list_of_dates):
    if start_date <= end_date:
        list_of_dates.append(start_date.strftime("%Y-%m-%d"))
        next_date = start_date + timedelta(days=1)
        walk_days(next_date, end_date, list_of_dates)


# Execute single data request with single URL fragment combination and single date
def get_data_for_fragment_on_date(fbSession, url, date):
    time.sleep(24)
    print('Getting ' + url.replace('{date}', date))
    return fbSession.get(url.replace('{date}', date)).text
    # return url.replace('{date}', date)  # for debugging, to check you got all your urls in the right arrangement


# Execute single data request with single URL fragment combination and single date
def get_filename_for_fragment_on_date(url, date):
    return get_filename_from_url_string(
        url.replace('{date}', date))  # for debugging, to check you got all your urls in the right arrangement


# Loop through all dates for single URL fragment combination
def get_all_dates_for_url(fbSession, url, dates):
    returnableObject = []
    if '{date}' in url:
        for date in dates:
            returnableObject.append(get_data_for_fragment_on_date(fbSession, url, date))
    else:
        returnableObject.append(get_data_for_fragment_on_date(fbSession, url, ''))
    return returnableObject


# Loop through all dates for single URL fragment combination
def get_all_dates_for_filenames(url, dates):
    returnableObject = []
    if '{date}' in url:
        for date in dates:
            returnableObject.append(get_filename_for_fragment_on_date(url, date))
    else:
        returnableObject.append(get_filename_for_fragment_on_date(url, ''))
    return returnableObject


# Loop through all URL fragment combinations
def get_all_data_for_all_urls(fbSession, url_lists, dates):
    returnableObject = []
    for url_list in url_lists:
        for url in url_list:
            returnableObject.append(get_all_dates_for_url(fbSession, url, dates))
    return returnableObject


# Loop through all URL fragment combinations
def get_all_filenames_for_all_urls(url_lists, dates):
    returnableObject = []
    for url_list in url_lists:
        for url in url_list:
            returnableObject.append(get_all_dates_for_filenames(url, dates))
    return returnableObject


def get_filename_from_url_string(url):
    return url.replace(
        fitbit_api_prefix, ''). \
        replace(fitbit_api_v1_0_fragment, ''). \
        replace(fitbit_api_v1_2_fragment, ''). \
        replace('/', '_'). \
        replace('-', '_')


# Construct list of all individual URL combinations, minus dates
def get_list_of_all_url_combinations_minus_dates(prefix, postfix,
                                                 v1_0, v1_2,
                                                 act_sum, act1min, act15min,
                                                 resources, sleep, heart,
                                                 goals_daily, goals_weekly):
    sleep_url = [prefix + v1_2 + sleep + postfix]
    heart_url = [prefix + v1_0 + heart + postfix]
    activity_summaries_url = [prefix + v1_0 + act_sum + postfix]
    goals = [prefix + v1_0 + goals_daily + postfix, prefix + v1_0 + goals_weekly + postfix]
    activities_1min = []
    for resource in resources:
        activities_1min.append(prefix + v1_0 + act1min.replace('{resource-path}', resource) + postfix)
    activities_15min = []
    for resource in resources:
        activities_15min.append(prefix + v1_0 + act15min.replace('{resource-path}', resource) + postfix)
    # return [goals, sleep_url, heart_url, activity_summaries_url, activities_1min, activities_15min]  # for >80 hrs runtime
    return [goals, sleep_url, heart_url, activity_summaries_url]  # for ~9 hrs runtime.
    # return [goals] # for debugging, to check it works all the way through with only 2 API requests (doesn't check proper URL formation with dates)


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
# needs_authorization = 'n'  # for when you need to run it and you already have the authorization token

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
    fitbit.token_from_fragment(str(
        'https://localhost#access_token=' + secret_codes_json['accessToken'] + '&state=' + secret_codes_json['state']))

# Request URL fragments
fitbit_api_prefix = 'https://api.fitbit.com'
fitbit_api_postfix = '.json'
fitbit_api_v1_0_fragment = '/1/user/-/'
fitbit_api_v1_2_fragment = '/1.2/user/-/'
fitbit_api_goals_daily_fragment = 'activities/goals/daily'
fitbit_api_goals_weekly_fragment = 'activities/goals/weekly'
fitbit_api_sleep_fragment = 'sleep/date/{date}'
fitbit_api_daily_activity_summary_fragment = 'activities/date/{date}'
fitbit_api_activities_1min_fragment = 'activities/{resource-path}/date/{date}/1d/1min'
fitbit_api_activities_15min_fragment = 'activities/{resource-path}/date/{date}/1d/15min'
fitbit_api_list_of_resource_path_fragments = ['calories',
                                              'caloriesBMR',
                                              'steps',
                                              'distance',
                                              'floors',
                                              'elevation',
                                              'minutesSedentary',
                                              'minutesLightlyActive',
                                              'minutesFairlyActive',
                                              'minutesVeryActive',
                                              'activityCalories']
fitbit_api_heart_fragment = 'activities/heart/date/{date}/1d'

file_output_dirs = {0: '../output/goalsDaily/',
                    1: '../output/goalsWeekly/',
                    2: '../output/sleep/',
                    3: '../output/heart/',
                    4: '../output/activities/',
                    5: '../output/calories_1min/',
                    6: '../output/caloriesBMR_1min/',
                    7: '../output/steps_1min/',
                    8: '../output/distance_1min/',
                    9: '../output/floors_1min/',
                    10: '../output/elevation_1min/',
                    11: '../output/minutesSedentary_1min/',
                    12: '../output/minutesLightlyActive_1min/',
                    13: '../output/minutesFairlyActive_1min/',
                    14: '../output/minutesVeryActive_1min/',
                    15: '../output/activityCalories_1min/',
                    16: '../output/calories_15min/',
                    17: '../output/caloriesBMR_15min/',
                    18: '../output/steps_15min/',
                    19: '../output/distance_15min/',
                    20: '../output/floors_15min/',
                    21: '../output/elevation_15min/',
                    22: '../output/minutesSedentary_15min/',
                    23: '../output/minutesLightlyActive_15min/',
                    24: '../output/minutesFairlyActive_15min/',
                    25: '../output/minutesVeryActive_15min/',
                    26: '../output/activityCalories_15min/'}

# Create list of dates to be queried
start_date = datetime(2017, 3, 24)
end_date = datetime(2018, 7, 13)
list_of_dates = []
walk_days(start_date, end_date, list_of_dates)

all_urls = get_list_of_all_url_combinations_minus_dates(fitbit_api_prefix, fitbit_api_postfix, fitbit_api_v1_0_fragment,
                                                        fitbit_api_v1_2_fragment,
                                                        fitbit_api_daily_activity_summary_fragment,
                                                        fitbit_api_activities_1min_fragment,
                                                        fitbit_api_activities_15min_fragment,
                                                        fitbit_api_list_of_resource_path_fragments,
                                                        fitbit_api_sleep_fragment,
                                                        fitbit_api_heart_fragment,
                                                        fitbit_api_goals_daily_fragment,
                                                        fitbit_api_goals_weekly_fragment)

all_filenames = get_all_filenames_for_all_urls(all_urls, list_of_dates)

all_data = get_all_data_for_all_urls(fitbit, all_urls, list_of_dates)

for i in range(len(all_filenames)):
    for j in range(len(all_filenames[i])):
        file = open(file_output_dirs.get(i) + all_filenames[i][j], 'x')
        file.write(all_data[i][j])
        file.close()

print("done")
