from common.adapters.redis import RedisCacheAdapter, BaseCacheHandler


class VideoSearchTermCacheHandler(BaseCacheHandler):

    BASE_KEY = "V2_VIDEO_SEARCH_TERM_{}"
    TIMEOUT = 10  # 60 * 15 in seconds
    MACHINE_ALIAS = "default"

    def __init__(self, hashed_query):
        print("hashed_query", hashed_query)
        key = self.BASE_KEY.format(hashed_query)
        print("key", key)
        super(VideoSearchTermCacheHandler, self).__init__(
            key,
            self.TIMEOUT,
            self.MACHINE_ALIAS
        )

        self.data = []

    def get_configuration(self):
        _cached_content = RedisCacheAdapter.get(
            self.key,
            machine_alias=self.MACHINE_ALIAS
        )

        if _cached_content:
            print('from cache')
            self.data = _cached_content["data"]

        return self.data