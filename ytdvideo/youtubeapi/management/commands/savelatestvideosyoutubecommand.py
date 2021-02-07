import time

from django.core.management import BaseCommand

from youtubeapi.helpers.savelatestvideoshelper import SaveLatestVideosHelper


class Command(BaseCommand):
    """
    python manage.py savelatestvideosyoutubecommand
    """
    COUNT = 0
    FETCH_VIDEOS_FREQUENCY_IN_SECS = 10

    def handle(self):
        while True:
            self.COUNT += 1
            self.save_latest_videos()
            time.sleep(self.FETCH_VIDEOS_FREQUENCY_IN_SECS)

    def save_latest_videos(self):
        print("save_latest_videos", self.COUNT, time.time())
        helper = SaveLatestVideosHelper()
        helper.save_videos_for_predefined_query_terms()
