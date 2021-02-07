from elasticsearch import exceptions


class BaseElasticModel(object):
    collection = None
    doc_type = None
    db_config_name = None
    adapter_class = None
    index_body = None

    @classmethod
    def create_collection(cls):
        """
        One time setup to create the required collection with required mappings...
        """
        index_create_params = {
            'index': cls.collection,
            'body': cls.index_body,
        }
        for _session in cls.sessions:
            _session.indices.create(**index_create_params)

    def __init__(self):
        error_message = "Please Add {variable_name}, Check adapters/elasticsearch/README.md for reference"
        assert self.collection is not None, error_message.format(variable_name="collection")
        assert self.doc_type is not None, error_message.format(variable_name="doc_type")
        assert self.db_config_name is not None, error_message.format(variable_name="db_config_name")
        assert self.adapter_class is not None, error_message.format(variable_name="adapter_class")
        assert self.index_body is not None, error_message.format(variable_name="index_body")

        self.adapter = self.adapter_class(self.db_config_name)
        self.write_sessions = self.adapter.get_write_sessions()
        self.read_session = self.adapter.get_read_session()
        self.all_sessions = self.adapter.get_all_sessions()

    def refresh_index(self):
        for session in self.all_sessions:
            session.indices.refresh(self.collection)

    def save(self, content, refresh=True):
        if 'id' not in content:
            raise ValueError("Id must be provided")

        for session in self.all_sessions:
            session.index(
                index=self.collection,
                doc_type=self.doc_type,
                body=content,
                id=content['id'],
                op_type="index",
                timeout="60s",
                refresh=str(refresh).lower()
            )

    def query(self, limit=10, offset=0, query_param=None, sort_params=None, size=None, **kwargs):
        data = {
            'count': 0,
            'result': []
        }
        try:
            _params = {
                "query": {
                    "match_all": {

                    }
                },
                "from": offset,
                "size": limit,
            }

            if query_param:
                del _params['query']
                _params.update(query_param)

            if sort_params:
                _params['sort'] = sort_params

            if size:
                _params['size'] = size

            cursor = self.read_session.search(
                index=self.collection,
                doc_type=self.doc_type,
                body=_params,
                filter_path=[
                    'hits.hits._id', 'hits.total', 'hits.hits._source'
                ]
            )

            if cursor['hits']['total'] == 0 or 'hits' not in cursor['hits']:
                return data
            else:
                data = {
                    'count': cursor['hits']['total']['value'],
                    'result': [obj["_source"] for obj in cursor['hits']['hits']]
                }

            return data
        except exceptions.NotFoundError:
            return data

    def delete(self, doc_id):
        for session in self.all_sessions:
            session.delete(
                index=self.collection,
                doc_type=self.doc_type,
                id=doc_id,
                refresh=True
            )

    def count(self, query_param=None):
        _params = {
            "query": {
                "match_all": {

                }
            }
        }

        if query_param:
            del _params['query']
            _params.update(query_param)
        try:
            cursor = self.read_session.count(
                index=self.collection,
                doc_type=self.doc_type,
                body=_params
            )

            data = cursor["count"]
        except:
            data = 0
        return data

    def update(self, id, partial_doc):
        doc = {
            "doc": partial_doc
        }
        for session in self.all_sessions:
            session.update(
                index=self.collection,
                doc_type=self.doc_type,
                body=doc,
                id=id
            )

    def get(self, id):
        result = self.read_session.get(
            index=self.collection,
            doc_type=self.doc_type,
            id=id
        )
        if result:
            return result["_source"]
        return None

    def update_by_query(self, body):
        """
        :param body:
        say you want to update a key("employer_name") for all records whose employer_id is 367888
        then body will be:
        {
            "script": {
                "inline": "ctx._source.employer_name='HAHAHA'",
                "lang": "painless"
            },
            "query": {
                "term": {"employer_id": {"value": 367682}}
            }
        }
        :return:
        {'took': 53, 'timed_out': False, 'total': 2, 'updated': 2, 'deleted': 0, 'batches': 1, 'version_conflicts': 0, 'noops': 0, 'retries': {'bulk': 0, 'search': 0}, 'throttled_millis': 0, 'requests_per_second': -1.0, 'throttled_until_millis': 0, 'failures': []}
        """
        for session in self.all_sessions:
            session.update_by_query(
                body=body,
                index=self.collection,
                doc_type=self.doc_type
            )

    def aggregate(self, aggs, query_param=None, size=0):
        """
        aggs = {'uniq_employer___you_may_put_any_name': {'terms': {'field': 'employer'}}}
        Result:
        {'aggregations': {'uniq_employer___you_may_put_any_name': {'doc_count_error_upper_bound': 0, 'sum_other_doc_count': 0, 'buckets': [{'key': 1, 'doc_count': 2}]}}}
        """
        _params = {
            'aggs': aggs,
            'size': size
        }
        if query_param:
            _params.update(query_param)

        return  self.read_session.search(
            index=self.collection,
            doc_type=self.doc_type,
            body=_params,
            filter_path=[
                'aggregations'
            ]
        )
