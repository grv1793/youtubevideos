from common.adapters.redis import RedisCacheAdapter


class BaseCacheHandler:
    BASE_KEY = None

    def __init__(self, key: str, timeout: int = 60, alias: str = "default"):
        self.key = key
        self.timeout = timeout
        self.machine_alias = alias

    def get_configuration(self):
        raise NotImplementedError('subclasses must provide this method')

    def set_configuration(self, content=None):
        if not content:
            raise Exception('no data while setting cache.')

        RedisCacheAdapter.set(
            self.key,
            content,
            timeout=self.timeout,
            machine_alias=self.machine_alias
        )

    def invalidate_cache(self):
        RedisCacheAdapter.delete(
            self.key,
            machine_alias=self.machine_alias
        )
