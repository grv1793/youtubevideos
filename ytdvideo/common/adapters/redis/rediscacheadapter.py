import traceback
from django.core.cache import caches


class RedisCacheAdapter:

    @staticmethod
    def set(key, value, timeout=None, machine_alias="default"):
        try:
            _key = key

            if timeout is None:
                _timeout = 60 * 1
            else:
                _timeout = timeout

            cache = caches[machine_alias]
            cache.set(_key, value, timeout=_timeout)
            return True
        except:
            print(traceback.format_exc())
            return False

    @staticmethod
    def get(key, machine_alias="default"):
        try:
            cache = caches[machine_alias]
            _value = cache.get(key)
        except:
            print(traceback.format_exc())
            _value = None

        return _value

    @staticmethod
    def delete(key, machine_alias="default"):
        try:
            cache = caches[machine_alias]
            cache.delete(key)
        except:
            print(traceback.format_exc())
            pass
