Here's an example of implementing a cache handler
~~~
from django.conf import settings

from common.adapters.redis import RedisCacheAdapter, BaseCacheHandler
from api.config.redisconfig import CacheConfig
from category.models import ShopCategory


class ShopCategoryCacheHandler(BaseCacheHandler):

    BASE_KEY = "GET_ALL_CATEGORIES"
    TIMEOUT = 60 * 60 * 24 * 365
    MACHINE_ALIAS = CacheConfig.DEFAULT

    def __init__(self):
        key = self.BASE_KEY

        super(ShopCategoryCacheHandler, self).__init__(
            key,
            self.TIMEOUT,
            self.MACHINE_ALIAS
        )

        self.shop_categories_data = []

    def get_configuration(self):
        _cached_content = RedisCacheAdapter.get(
            self.key,
            machine_alias=self.MACHINE_ALIAS
        )

        if _cached_content:
            print('from cache')
            self.shop_categories_data = _cached_content["shop_categories_data"]
        else:
            print('from db')
            shop_categories = ShopCategory.objects.using(
                settings.DATABASE_TYPE.RDS_REPLICA_1
            ).all()

            self.shop_categories_data = list(shop_categories.values('id', 'display_name'))
            self.set_configuration({
                "shop_categories_data": self.shop_categories_data
            })

        return self.shop_categories_data
~~~