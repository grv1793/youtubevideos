# Requirements:
~~~
https://fampay.notion.site/fampay/Backend-Assignment-FamPay-32aa100dbd8a4479878f174ad8f9d990
~~~

# System Design:
~~~
Refer current directory 
----  youtubevideos/system-design.png file
~~~

# Project Directory:
~~~
cd youtubevideos/ytdvideo

Run All commands mentioned below in this directory
~~~

# Start Docker Containers:
~~~
run ./startdockerserver.sh

docker ps
# You should be able to see docker containers

~~~

# Add Youtube Api Keys portal:
~~~
you can configure the Youtube API keys here:
http://127.0.0.1:80/portal/fetchyoutubedata/youtubevideoapikey/

Adding/Deletion of api keys can be done in runtime

You will see that API keys will be automatically set to InActive in portal post limit is reached.
~~~

# Fetch Youtube data Service:
~~~
Save youtube videos after every 30 seconds

you can see the logs using this command:
-> docker-compose logs --tail="all" -f save_latest_video_content_command

Implementation:
1. added django management command to execute this
2. management command executed in docker container
3. Check file youtubevideos/ytdvideo/fetchyoutubedata/management/commands/savelatestvideosyoutubecommand.py
4. Fetches videos data from youtube apis
5. saves data in Video and VideoThumnail tables of postgres
6. The data is saved in ElasticSearch as well
~~~

# Get Stored Videos with/without filter (title, description)
~~~
Implementation:
1. Check Cache
2. if data in cache present, get result from cache
3. Else: Get Result from ElasticSearch.
4. Apply pagination on the Result
5. send response

~~~

# Postman Collection json file:
~~~
check this file in repository:
youtubevideos/ytdvideo/youtubevideos.postman_collection.json

Go to postman and import postman collection using this file.
~~~


