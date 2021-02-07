from common.adapters.elasticsearch.baseelasticmodel import BaseElasticModel
from common.adapters.elasticsearch.elasticsearchdbmultinodeclusteradapter import ElasticSearchDBMultiNodeClusterAdapter


class ESVideo(BaseElasticModel):
    collection = "api_video"
    doc_type = "video"
    db_config_name = "elastic_search_cluster"  # got value from django settings.NOSQL_DATABASES
    adapter_class = ElasticSearchDBMultiNodeClusterAdapter
