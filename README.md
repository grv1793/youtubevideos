# youtubevideos

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
Postman Collection json file:

check this file in repository:
youtubevideos/ytdvideo/youtubevideos.postman_collection.json

Go to postman and import postman collection using this file.
~~~

~~~
Save youtube videos after every 10 seconds

Implementation:
1. added management command to execute this
2. management command executed in docker container
3. Check file youtubevideos/ytdvideo/youtubeapi/management/commands/savelatestvideosyoutubecommand.py
4. Fetches videos data from youtube apis
5. saves data in Video and VideoThumnail tables of postgres
6. The data is saved in ElasticSearch as well
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
