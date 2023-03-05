import base64
import hashlib
import json
from api.cachehandlers.videosearchtermcachehandler import VideoSearchTermCacheHandler
from api.helpers.elasticmodelhelpers.videoelasticmodelhelper import VideoElasticModelHelper
from api.mixins.listmodelesmixin import ListModelESMixin
from common.helpers.paginationhandler import ArrayPaginate


class VideoController(ListModelESMixin):
    es_model_helper = VideoElasticModelHelper
    paginate = False

    def __init__(self, request):
        self.request = request
        self.query_params = self.request.query_params
        self.hashed_query = None
        self.process_request()

        super(VideoController, self).__init__(self.query_params)

    def process_request(self):
        if self.request.query_params.get("search_term"):
            self.hashed_query = self.request.query_params.get("search_term").replace(" ", "_")

    def get_response_data(self, *args, **kwargs):
        data = self.get_data_from_cache()
        if not data:
            data = self.list(*args, **kwargs)
            self.save_data_in_cache(data)

        _pagination_handler = ArrayPaginate(data, self.request)
        _paginated_data = _pagination_handler.fetch()

        return {
            "data": _paginated_data["data"],
            "next": _paginated_data["next"],
            "prev": _paginated_data["prev"],
            "count": _paginated_data["count"],
        }

    def get_data_from_cache(self):
        cache_handler = VideoSearchTermCacheHandler(self.hashed_query)
        return cache_handler.get_configuration()

    def get_query(self):
        query = {"bool": {"should": []}}

        if self.query_params:
            if self.query_params.get("search_term"):
                title_should_query = self.es_model_helper.get_widcard_and_fuzzy_query(
                    ["title"],
                    self.query_params.get("search_term"),
                )
                query = self.es_model_helper.form_query(title_should_query, query, query_type="should")

                description_should_query = self.es_model_helper.get_widcard_and_fuzzy_query(
                    ["description"],
                    self.query_params.get("search_term"),
                )
                query = self.es_model_helper.form_query(description_should_query, query, query_type="should")

        return {'query': query}

    def get_sort_params(self):
        if self.query_params.get("search_term"):
            return

        sort_params = {"published_at": {"order": "desc"}}
        return sort_params

    def list_via_db(self, query_params, *args, **kwargs):
        # TODO
        print("override this method")
        return []

    def save_data_in_cache(self, data):
        cache_handler = VideoSearchTermCacheHandler(self.hashed_query)
        return cache_handler.set_configuration(
            content={
                "data": data
            }
        )

    # @staticmethod
    # def decode_base_64(query_params):
    #     """
    #
    #     :param query_params: base64encoded string having filter and search params
    #     :return:
    #     """
    #     try:
    #         base64_bytes = query_params.encode('ascii')
    #         message_bytes = base64.b64decode(base64_bytes)
    #         message = message_bytes.decode('ascii')
    #
    #         hasher = hashlib.sha256(query_params.encode())
    #         hash_string = hasher.hexdigest()
    #         return message, hash_string
    #     except:
    #         return None, None
