import copy
import traceback


class ListModelESMixin:
    """
    List a queryset.
    Need to define `get_query` and `to_json` methods in the view.
    `to_json(self, )` method is the data that will be sent in the response.
    Need to define `es_model_helper`
    `es_model_helper` must define a `filter method` to query ElasticSearch
    """

    es_model_helper = None
    limit = 10000
    offset = 0
    paginate = True

    def __init__(self, query_params):
        self.query_params = query_params

    def to_json(self, data):
        return data

    def get_query(self):
        query = {"query": {"match_all": {}}}
        sort_params = self.get_sort_params()
        if sort_params:
            query["sort"] = sort_params
        return query

    def get_sort_params(self):
        return

    def list(self, *args, **kwargs):
        try:
            pagination_config = self.pagination_config()

            assert getattr(self, "es_model_helper") is not None
            assert getattr(self.es_model_helper, "filter") is not None

            query = self.get_query()
            sort_params = self.get_sort_params()
            data = self.es_model_helper().filter(
                query,
                pagination_config,
                sort_params=sort_params,
                paginate=self.paginate
            )
            if not self.paginate:
                data = data['result']

            return self.to_json(data)
        except Exception as e:
            print(traceback.format_exc())
            print("Elastic Search Error-ed out. Fetching results from DB")
            # # Fallback to DB query
            return self.list_via_db(self.query_params, *args, **kwargs)

    def list_via_db(self, query_params, *args, **kwargs):
        raise NotImplementedError

    def pagination_config(self, config={}):
        if type(config) != dict:
            config = config.dict()

        if config.get("limit"):
            config["limit"] = int(config["limit"])
        else:
            config["limit"] = self.limit

        if config.get("offset"):
            config["offset"] = int(config["offset"])
        else:
            config["offset"] = self.offset

        return config
