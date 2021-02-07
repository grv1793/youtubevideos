from common.adapters.redis import RedisCacheAdapter, BaseCacheHandler
from youtubeapi.models import YoutubeVideoAPIKey


class YouTubeAPIKeyCacheHandler(BaseCacheHandler):

    BASE_KEY = "ACTIVE_API_KEY"
    TIMEOUT = 60 * 60  # in seconds
    MACHINE_ALIAS = "default"

    def __init__(self):
        key = self.BASE_KEY
        super(YouTubeAPIKeyCacheHandler, self).__init__(
            key,
            self.TIMEOUT,
            self.MACHINE_ALIAS
        )

        self.api_key = None

    def get_configuration(self):
        _cached_content = RedisCacheAdapter.get(
            self.key,
            machine_alias=self.MACHINE_ALIAS
        )

        if _cached_content:
            print('from cache')
            self.data = _cached_content
        else:
            api_key = YoutubeVideoAPIKey.objects.filter(
                status=YoutubeVideoAPIKey.STATUS_CHOICES._identifier_map.get(YoutubeVideoAPIKey.ACTIVE)
            ).first()
            if api_key:
                self.set_configuration(api_key.key)

        return self.api_key
