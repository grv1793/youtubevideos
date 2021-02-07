from common.adapters.elasticsearch.baseelasticmodelhelper import BaseElasticModelHelper

from api.elasticmodels.video import ESVideo
from api.models import Video
from api.helpers.modelhelpers.videomodelhelper import VideoModelHelper


class VideoElasticModelHelper(BaseElasticModelHelper):
    model_helper = VideoModelHelper
    es_model = ESVideo

    @staticmethod
    def get_should_query():
        return {"bool": {"should": []}}
