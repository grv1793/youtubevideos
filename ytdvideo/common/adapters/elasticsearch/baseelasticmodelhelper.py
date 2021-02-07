from common.adapters.elasticsearch.espaginate import ESPaginate


class BaseElasticModelHelper(object):

    model_helper = None
    es_model = None

    def __init__(self):
        assert self.model_helper is not None, "No Model Helper"
        assert self.es_model is not None, "No ES Model"

    def refresh_index(self):
        self.es_model().refresh_index()

    def push_obj_to_es(self, obj):
        data = self.model_helper.get_obj_data(obj)
        self.es_model(content=data).save()

    def filter(self, query, pagination_config=None, sort_params=None, paginate=True):
        if not pagination_config:
            pagination_config = {
                'limit': 10000,
                'offset': 0
            }
            paginate = False
        if paginate:
            paginated_candidate = ESPaginate(
                self.es_model,
                pagination_config,
                query,
                sort_params
            )
            return paginated_candidate.fetch()

        return self.es_model().query(query_param=query, sort_params=sort_params, **pagination_config)

    @staticmethod
    def parse_es_result(data):
        # to be overridden in the child class
        return data

    @staticmethod
    def get_widcard_and_fuzzy_query(fields, search_term, max_boost=100, boost_diff=20, lowest_boost=50):
        should_query = []

        for field in fields:
            query_wildcard = {
                "wildcard": {
                    field: {
                        "value": f"*{search_term}*",
                        "boost": max_boost
                    }
                }
            }
            should_query.append(query_wildcard)

        for field in fields:
            term_list = search_term.split(" ")
            term_list_length = len(term_list)
            if term_list_length > 1:
                boost = max_boost
                for i in range(term_list_length):
                    boost = boost - boost_diff;
                    if boost > lowest_boost:
                        should_query.append({
                            "wildcard": {
                                field: {
                                    "value": f"*{term_list[i]}*",
                                    "boost": boost
                                }
                            }
                        })
                    else:
                        break

        query_fuzzy = {
            "multi_match": {
                "query": search_term,
                "fields": fields,
                "fuzziness": "AUTO"
            }
        }

        query_match_phrase = {
            "multi_match": {
                "query": search_term,
                "fields": fields,
                "type": "phrase",
                "slop": 3
            }
        }

        should_query.append(query_fuzzy)
        should_query.append(query_match_phrase)
        return should_query

    def get_count(self, query):
        try:
            return self.es_model().count(query_param=query)
        except:
            return 0

    def update_model_es_data(self, obj):
        data = self.model_helper.get_obj_data(obj)
        data.pop('id', None)
        self.es_model().update(obj.id, data)

    def update(self, id, data):
        self.es_model().update(id, data)

    @staticmethod
    def join_must_and_should_queries(must_query, should_query):
        query = {"bool": {"should": [], "must": []}}
        query["bool"]["should"] = should_query["bool"]["should"]
        query["bool"]["must"] = must_query["bool"]["must"]

        return query

    @staticmethod
    def form_query(query, existing_query=None, query_type="must"):
        """
        >>> query1 = { "terms": { "job_id": [6, 7] } }
        >>> temp = EcsCandidateHelper.form_child_query(query1)
        {'bool': {'must': [{'terms': {'job_id': [6, 7]}}]}}

        >>> query2 = { "match": {"current_status": "Have not talked"}}
        >>> EcsCandidateHelper.form_child_query(query2, temp)
        {'bool': {'must': [{'terms': {'job_id': [6, 7]}},
            {'match': {'current_status': 'Have not talked'}}]}}
        """
        if not existing_query:
            query = {"bool": {query_type: [query]}}
            return query

        if type(query) == list:
            try:
                existing_query["bool"][query_type] += query
            except:
                existing_query["bool"][query_type] = query
        else:
            existing_query["bool"][query_type].append(query)

        return existing_query

    @staticmethod
    def get_query_for_date_range(field, date_range):
        return {
            "range": {field: {"gte": date_range[0], "lte": date_range[1]}}
        }

    def aggregate(self, aggs, get_count=False, query_param=None, size=0):
        try:
            aggs_key = list(aggs.keys())[0]
        except:
            return []

        data = self.es_model().aggregate(aggs, query_param=query_param, size=size)
        data = data['aggregations'][aggs_key]['buckets']

        if get_count:
            return len(data)

        return data

    def get_sum_of_field(self, field, query_param):
        aggs_key = f"sum_{field}"
        aggs = {aggs_key: {"sum": {"field": field}}}
        data = self.es_model().aggregate(aggs, query_param=query_param)
        return data['aggregations'][aggs_key]['value']

    def bulk_delete(self, doc_ids):
        # TODO add bulk delete in elastic model
        for doc_id in doc_ids:
            self.es_model().delete(doc_id)
