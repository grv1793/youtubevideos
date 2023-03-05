import time

from django.core.management import BaseCommand

from django.contrib.auth.models import User
from fetchyoutubedata.configs.youtubeapikeys import YTD_API_KEYS
from fetchyoutubedata.models.youtubevideosapikey import YoutubeVideoAPIKey
from fetchyoutubedata.helpers.savelatestvideoshelper import SaveLatestVideosHelper


class Command(BaseCommand):
    """
    python manage.py savelatestvideosyoutubecommand
    """
    COUNT = 0
    FETCH_VIDEOS_FREQUENCY_IN_SECS = 60

    def handle(self, *args, **kwargs):
        print("On Sleep for 30 seconds")
        time.sleep(30)

        self.create_initial_data()

        while True:
            self.COUNT += 1
            self.save_latest_videos()

            time.sleep(self.FETCH_VIDEOS_FREQUENCY_IN_SECS)

    def create_initial_data(self):
        self.create_superuser()
        self.create_youtube_api_keys()

    def save_latest_videos(self):
        print("save_latest_videos", self.COUNT, time.time())
        helper = SaveLatestVideosHelper()
        helper.save_videos_for_predefined_search_terms()

    def create_superuser(self):
        try:
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        except:
            pass

    def create_youtube_api_keys(self):
        for key in YTD_API_KEYS:
            YoutubeVideoAPIKey.objects.get_or_create(key=key)
