# fitbit Data Analyser

> all the following is correct at time of commit

###Useful Info:
####Tutorial: 
Where the oauth2 code is largely copied from: https://requests-oauthlib.readthedocs.io/en/latest/examples/fitbit.html

#### API paths
https://dev.fitbit.com/build/reference/web-api/explore/ \
(Scroll down to section 'Time Series' for what you're really interested in.)

#### Date Format
YYYY-mm-dd

#### Rate limit
150 per hour.\
See response headers for real time data on where you're up to with that. 

#### Resource Path Options
##### ACTIVITY
activities/calories
activities/caloriesBMR
activities/steps
activities/distance
activities/floors
activities/elevation
activities/minutesSedentary
activities/minutesLightlyActive
activities/minutesFairlyActive
activities/minutesVeryActive
activities/activityCalories

##### TRACKER ACTIVITY
activities/tracker/calories
activities/tracker/steps
activities/tracker/distance
activities/tracker/floors
activities/tracker/elevation
activities/tracker/minutesSedentary
activities/tracker/minutesLightlyActive
activities/tracker/minutesFairlyActive
activities/tracker/minutesVeryActive
activities/tracker/activityCalories

#### Time Series API Calls
GET /1/user/-/activities/{resource-path}/date/{base-date}/{end-date}.json : Get Activity Time Series\
GET /1/user/-/activities/tracker/{resource-path}/date/{base-date}/{end-date}.json : Get Activity Time Series\
GET /1/user/-/activities/{resource-path}/date/{date}/{period}.json : Get Activity Time Series\
GET /1/user/-/activities/tracker/{resource-path}/date/{date}/{period}.json : Get Activity Time Series\
GET /1/user/-/activities/{resource-path}/date/{base-date}/{end-date}/{detail-level}.json : Get Intraday Time Series\
GET /1/user/-/activities/{resource-path}/date/{date}/1d/{detail-level}.json : Get Intraday Time Series\
GET /1/user/-/activities/{resource-path}/date/{date}/{end-date}/{detail-level}/time/{start-time}/{end-time}.json : Get Intraday Time Series\
GET /1/user/-/activities/{resource-path}/date/{date}/1d/{detail-level}/time/{start-time}/{end-time}.json : Get Intraday Time Series\
GET /1/user/-/body/{resource-path}/date/{date}/{period}.json : Get Body Time Series\
GET /1/user/-/body/{resource-path}/date/{base-date}/{end-date}.json : Get Body Time Series\
GET /1/user/-/foods/log/{resource-path}/date/{base-date}/{end-date}.json : Get Food or Water Time Series\
GET /1/user/-/foods/log/{resource-path}/date/{date}/{period}.json : Get Food or Water Time Series\
GET /1/user/-/activities/heart/date/{date}/{period}.json : Get Heart Rate Time Series\
GET /1/user/-/activities/heart/date/{base-date}/{end-date}.json : Get Heart Rate Time Series\
GET /1/user/-/activities/heart/date/{date}/{end-date}/{detail-level}.json : Get Heart Rate Intraday Time Series\
GET /1/user/-/activities/heart/date/{date}/{end-date}/{detail-level}/time/{start-time}/{end-time}.json : Get Heart Rate Intraday Time Series\
GET /1/user/-/activities/heart/date/{date}/1d/{detail-level}.json : Get Heart Rate Intraday Time Series\
GET /1/user/-/activities/heart/date/{date}/1d/{detail-level}/time/{start-time}/{end-time}.json : Get Heart Rate Intraday Time Series