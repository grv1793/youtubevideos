# youtubevideos
~~~
Requirements: https://www.notion.so/Backend-Assignment-FamPay-32aa100dbd8a4479878f174ad8f9d990
~~~

~~~
Go to a dir in your system and run following commands:

git clone https://github.com/grv1793/youtubevideos.git
cd youtubevideos/ytdvideo
run ./startdockerserver.sh

docker ps
# You should be able to see docker containers

~~~

~~~
Create Super user

1. run: docker-compose exec api bash -c "python3 manage.py createsuperuser"

you will be asked to fill following details:

Username (leave blank to use 'root'): <enter username - eg: admin>
Email address: <enter email - eg: grv1793@gmail.com>
Password: <enter password - eg: admin>
Password (again): <enter password - eg: admin> 
Superuser created successfully.
~~~

~~~
Go to 
http://127.0.0.1:3000/api/portal/

enter username and password

you will see dashboard for videos or go to http://127.0.0.1:3000/portal/api/video/
~~~

~~~
you can configure the Youtube API keys here:
http://127.0.0.1:3000/portal/youtubeapi/youtubevideoapikey/

Adding/Deletion of api keys can be done in runtime
some of the API Keys that can be used are: 
1. AIzaSyAv5hny1k5pP59AhnyePiANcAhAImOuiiU
2. AIzaSyBDBKr6k0acy5RfoyAXhKf1gWikeZQOfUw
3. AIzaSyDUzlTQ-ZkNxSrOTpWqhUfACANuJ8G77n8
4. AIzaSyB-lY-psYHDqny-UhnlT4QyaP5HLMhEX3U

Note: Videos data will be stored post addition of above API Keys in Django portal

You will see that API keys will be automatically set to InActive in portal.
~~~

~~~
Save youtube videos after every 10 seconds

Once you have configured the API Keys in Portal
you can see the logs using this command:
-> docker-compose logs --tail="all" -f save_latest_video_content_command

Implementation:
1. added django management command to execute this
2. management command executed in docker container
3. Check file youtubevideos/ytdvideo/youtubeapi/management/commands/savelatestvideosyoutubecommand.py
4. Fetches videos data from youtube apis
5. saves data in Video and VideoThumnail tables of postgres
6. The data is saved in ElasticSearch as well
~~~

~~~
Postman Collection json file:

check this file in repository:
youtubevideos/ytdvideo/youtubevideos.postman_collection.json

Go to postman and import postman collection using this file.
~~~

~~~
Get Stored Videos with/without filter (title, description)

Implementation:
1. Check Cache
2. if cache present, get result from cache
3. Else: Get Result from ElasticSearch.
4. Apply pagination on the Result
5. send response

~~~
