import datetime
from common.adapters.redis import RedisCacheAdapter, BaseCacheHandler
from fetchyoutubedata.models.searchtermpublishedaftertimestamp import SearchTermPublishedAfterTimestamp


class LastPublishedAfterTimestampCacheHandler(BaseCacheHandler):

    BASE_KEY = "last_published_after_timestamp_{}"
    TIMEOUT = 10  # 60 * 15 in seconds
    MACHINE_ALIAS = "default"
    DEFAULT_PUBLISHED_AFTER_TIMESTAMP = datetime.datetime(2022, 1, 1)

    def __init__(self, search_term):
        self.search_term = search_term
        self.key = self.BASE_KEY.format(search_term)
        super(LastPublishedAfterTimestampCacheHandler, self).__init__(
            self.key,
            self.TIMEOUT,
            self.MACHINE_ALIAS
        )

        self.last_published_after_timestamp = None

    def get_configuration(self):
        _cached_content = RedisCacheAdapter.get(
            self.key,
            machine_alias=self.MACHINE_ALIAS
        )

        if _cached_content:
            print('from cache')
            self.last_published_after_timestamp = _cached_content["data"]
        else:
            self.last_published_after_timestamp = self.fetch_from_db()

        return self.last_published_after_timestamp

    def set_configuration(self, published_after=None):
        super(LastPublishedAfterTimestampCacheHandler, self).set_configuration(published_after)
        self.update_search_term_published_after_timestamp_in_db(published_after)

    def update_search_term_published_after_timestamp_in_db(self, published_after):
        obj = SearchTermPublishedAfterTimestamp.objects.filter(
            search_term=self.search_term
        ).last()
        if obj:
            obj.published_after = published_after
            obj.save()
        else:
            SearchTermPublishedAfterTimestamp.objects.create(
                search_term=self.search_term,
                published_after=published_after
            )

    def fetch_from_db(self):
        obj = SearchTermPublishedAfterTimestamp.objects.filter(
            search_term=self.search_term
        ).last()
        if obj:
            return obj.published_after

        return self.DEFAULT_PUBLISHED_AFTER_TIMESTAMP
