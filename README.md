
Summary – web api for downloading xkcd comics (https://xkcd.com) based on date. XKCD provides an API for convenient use, see their ‘About’ section.

Write an application (API, no front) in Flask/Connexion.
**Base flow**
i. User send request providing a date in format DDMMYYYY
ii. Your application should connect to xkcd and download metadata and image with comic.
iii. You should store metadata file and image; use two different types of store (database and filesystem)
iv. Return response to user (image)

**Statistics endpoint**
i. User sends id of a comic, in return should get number of how many times it was requested

**Dockerize application**
The same application as an AWS Lambda function
Base requirement is that lambda code is complete, there is no need to deploy it
i. Use DynamoDB and S3 to store data       

Additionally, if you’ll be able:
 i. add terraform that creates infrastructure – use API Gateway as a receiver of requests

ii. add tests


**API Documentation**

Get comic by date API

**API - 1** 

/comic-by-date/{date}

Method - POST

Parameters - date in DDMMYYYY format

URL - http://127.0.0.1:5000/api/comic-by-date/09062023

Description - Get comic by date, as xkcd only allows to get comic by id, 
this API converts the date to id as per publishers schedule (Monday, Wednesday, Friday) and returns the comic. 
as data inconsistent in xkcd so this API will only provide information from 2023.

**API - 2**

/comic-by-id/{comic_id}

Method - POST

Parameters - comic_id

URL - http://127.0.0.1:5000/api/comic-by-id/2787

Description - Get comic by id, as xkcd only allows to get comic by id.

**API - 3**

/comic-using-soup/{date}

Method - POST

Parameters - date in DDMMYYYY format

URL - http://127.0.0.1:5000/api/comic-using-soup/09062023

Description - Alternative approach of fetching comic by date using beautiful soup as 
xkcd only allows to get comic by id,

**API - 4**

/comic-statistics/{comic_id}

Method - GET

Parameters - comic_id

URL - http://127.0.0.1:5000/api/comic-statistics/2787

Description - Get comic statistics by id from dynamodb


Use postman or http://127.0.0.1:5000/api/ui/ to test the APIs

**Update .env**
AWS_ACCESS_KEY_ID='fakeMyKeyId'
AWS_SECRET_ACCESS_KEY='fakeSecretAccessKey'
REGION_NAME='us-west-2'
ENDPOINT_URL='http://localhost:8000'
with you AWS access Key
