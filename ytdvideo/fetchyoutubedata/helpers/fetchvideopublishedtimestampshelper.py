from django.utils import timezone
from api.cachehandlers.lastpublishedaftertimestampcachehandler import LastPublishedAfterTimestampCacheHandler


class FetchVideoPublishedTimestampsHelper(object):

    def __init__(self, search_term):
        ch = LastPublishedAfterTimestampCacheHandler(search_term)
        self.published_after = ch.get_configuration()
        self.published_before = timezone.now()
        self.search_term = search_term

    def get_published_after_timestamp(self):
        return self.published_after.strftime('%Y-%m-%dT%H:%M:%SZ')

    def get_published_before_timestamp(self):
        return self.published_before.strftime('%Y-%m-%dT%H:%M:%SZ')

    def update_published_after_timestamp(self):
        ch = LastPublishedAfterTimestampCacheHandler(self.search_term)
        ch.set_configuration(self.published_before)
