import time

from django.core.management import BaseCommand

from youtubeapi.helpers.savelatestvideoshelper import SaveLatestVideosHelper


class Command(BaseCommand):
    """
    python manage.py savelatestvideosyoutubecommand
    """
    COUNT = 0
    FETCH_VIDEOS_FREQUENCY_IN_SECS = 10
    MAX_API_CALL_LIMIT = 2

    def handle(self, *args, **kwargs):
        print("On Sleep for 30 seconds")
        time.sleep(30)
        while True:
            if self.COUNT > self.MAX_API_CALL_LIMIT:
                print("MAX_API_CALL_LIMIT Reached: {}".format(self.COUNT))
                self.COUNT += 1
                time.sleep(self.FETCH_VIDEOS_FREQUENCY_IN_SECS)
                continue

            self.COUNT += 1
            self.save_latest_videos()
            time.sleep(self.FETCH_VIDEOS_FREQUENCY_IN_SECS)

    def save_latest_videos(self):
        print("save_latest_videos", self.COUNT, time.time())
        helper = SaveLatestVideosHelper()
        helper.save_videos_for_predefined_query_terms()
