example:

import pymongo
from basemodels.adapter.mongodblog import MongoDBLogAdapter
from basemodels.adapter.mongodblongterm import MongoDBLongTermAdapter
from basemodels.mongomodels.v2.mongomodel import MongoModel, MongoCollection, MongoIndex
from basemodels.utils.datetimeutil import get_server_timestamp


class CandidateRYCSMS(MongoModel):
    collection = MongoCollection('candidate_ryc_sms', indices=[
        MongoIndex("candidate_id", unique=True),
        MongoIndex([("timestamp", pymongo.DESCENDING)])
    ], save_filter=['candidate_id'])

    def __init__(self):
        super().__init__(MongoDBLogAdapter, self.collection)


