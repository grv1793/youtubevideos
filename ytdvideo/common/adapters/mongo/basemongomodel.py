from copy import deepcopy
from datetime import datetime
import time
from typing import List


class MongoIndex(object):
    def __init__(self, keys, **kwargs):
        """
        Define an index for a collection

        Takes either a single key or a list of (key, direction) pairs.
        The key(s) must be an instance of :class:`basestring`
        (:class:`str` in python 3), and the direction(s) must be one of
        (:data:`~pymongo.ASCENDING`, :data:`~pymongo.DESCENDING`,
        :data:`~pymongo.GEO2D`, :data:`~pymongo.GEOHAYSTACK`,
        :data:`~pymongo.GEOSPHERE`, :data:`~pymongo.HASHED`,
        :data:`~pymongo.TEXT`).

        To create a single key ascending index on the key ``'mike'`` we just
        use a string argument::

           MongoIndex("mike")

        For a compound index on ``'mike'`` descending and ``'eliot'``
        ascending we need to use a list of tuples::

           MongoIndex([("mike", pymongo.DESCENDING),
                       ("eliot", pymongo.ASCENDING)])

        Valid kwargs include, but are not limited to:

          - `name`: custom name to use for this index - if none is
            given, a name will be generated.
          - `unique`: if ``True`` creates a uniqueness constraint on the index.
          - `background`: if ``True`` this index should be created in the
            background.
          - `sparse`: if ``True``, omit from the index any documents that lack
            the indexed field.
          - `bucketSize`: for use with geoHaystack indexes.
            Number of documents to group together within a certain proximity
            to a given longitude and latitude.
          - `min`: minimum value for keys in a :data:`~pymongo.GEO2D`
            index.
          - `max`: maximum value for keys in a :data:`~pymongo.GEO2D`
            index.
          - `expireAfterSeconds`: <int> Used to create an expiring (TTL)
            collection. MongoDB will automatically delete documents from
            this collection after <int> seconds. The indexed field must
            be a UTC datetime or the data will not expire.
          - `partialFilterExpression`: A document that specifies a filter for
            a partial index.
        """

        self.keys = keys
        self.__dict__.update(kwargs)


class MongoCollection(object):

    def __init__(self, name: str, indices: List[MongoIndex] = None, save_filter: List[str] = None):
        """
        Define Mongo Collection

        Takes name of mongo collection, list of indices (if any)
        and save_filter parameter used when saving a document

          - name : String name of a mongo collection
          - indices : A List of MongoIndex
          - save_filter : A dictionary which used when saving a document. They key, value in `save_filter` dict is used
              to find an existing document to update. They value in a `save_filter' key is searched in the document to
              be stored, based on the content, search is made in mongo before inserting. If a document exists, it gets
              updated. A KeyError is throw if given `save_filter` key is not present in given document.
              Passing a `None` value to save_filter will save the document without checking for existing documents.
        """

        if indices is None:
            indices = []

        self.name = name
        self.indices = indices
        self.save_filter = save_filter

    def get_save_filter(self, content: dict):
        """
        This is a helper method that generates the filter dict used before saving a document
        """
        _filter = dict()

        for k in self.save_filter:
            if k not in content:
                raise KeyError('Required key `{key}` not found in the document'.format(key=k))
            _filter[k] = content[k]

        return _filter


class MongoModel:
    SERVER_TIMESTAMP = 'server_timestamp'

    def __init__(self, adapter, db_config_name, collection: MongoCollection, **kwargs):
        """
        MongoModel to be used as parent class for generating / managing mongo models

        - adapter : An adapter can be any class from below
            MongoDBAdapter, MongoDBLogAdapter, MongoDBLongTermAdapter, MongoDBWebsiteAdapter
        - collection : An instance of `MongoCollection`

        Available kwargs:
        - instance_type : Define the instance type to be used for get_session(instance)
        """
        self.adapter = adapter(db_config_name)
        self.collection = collection

        self.write_session = self.adapter.get_all_sessions(db_config_name)
        self.read_session = self.adapter.get_read_session(db_config_name)

        self.write_cursor = self.write_session[self.collection.name]
        self.read_cursor = self.read_session[self.collection.name]

    def __set_indices(self):
        is_server_timestamp_indexed = False

        for index in self.collection.indices:
            kwargs = deepcopy(index.__dict__)

            del kwargs['keys']
            if 'background' not in kwargs:
                kwargs['background'] = True

            self.write_cursor.create_index(index.keys, **kwargs)

            if type(index.keys) == self.SERVER_TIMESTAMP:
                is_server_timestamp_indexed = True
            elif type(index.keys) == List:
                for key in index.keys:
                    if key[0] == self.SERVER_TIMESTAMP:
                        is_server_timestamp_indexed = True

        if not is_server_timestamp_indexed:
            self.write_cursor.create_index(self.SERVER_TIMESTAMP, background=True)

    def save(self, content):
        """
        Insert or update a single document

         - content : The document to be save

         Note: If the collection has defined a `save_filter`, then all keys required by the `save_filter`
         must be present in content
        """

        if self.SERVER_TIMESTAMP not in content:
            content[self.SERVER_TIMESTAMP] = int(time.mktime(datetime.utcnow().timetuple()))

        if self.collection.save_filter:
            _filter = self.collection.get_save_filter(content)
            cursor = self.write_cursor.find_one(_filter)

            if cursor:
                # Update document
                self.write_cursor.update(_filter, content)
            else:
                self.write_cursor.insert_one(content)
        else:
            self.write_cursor.insert_one(content)

        self.__set_indices()

    def update(self, filter_params, data):
        """
        Update one document at a time
        """
        self.write_cursor.update(filter_params, {"$set": data})

    def update_many(self, filter_params, data):
        """
        Update all documents which match filter_params
        """
        self.write_cursor.update_many(filter_params, {"$set": data})

    def filter(self, **kwargs):
        """
        Filter mongo documents

        Defined keyword args used for operation:
        - limit : Limit number of documents returned from query result
        - offset : Skip the first `offset` results from query result
        - sort : List of (key, direction) pairs specifying the keys to sort on.
                    Eg. [('field1', pymongo.ASCENDING), ('field2', pymongo.DESCENDING)]
        - exclude_fields : List of `strings` to be removed from filter output
        """

        _limit = 10
        _offset = 0
        _sort = []
        _exclude_fields = []

        if 'limit' in kwargs:
            _limit = kwargs.pop('limit')

        if 'offset' in kwargs:
            _offset = kwargs.pop('offset')

        if 'sort' in kwargs:
            _sort = kwargs.pop('sort')

        if 'exclude_fields' in kwargs:
            _exclude_fields = kwargs.pop('exclude_fields')

        cursor = self.read_cursor.find(kwargs).limit(_limit).skip(_offset)

        if _sort:
            cursor = cursor.sort(_sort)
        data = []

        for c in cursor:
            c.pop('_id', None)
            if _exclude_fields:
                for field in _exclude_fields:
                    c.pop(field, None)
            data.append(c)

        return data

    def count(self, **kwargs):
        """
        Count filtered documents
        """
        return self.read_cursor.count(kwargs)

    def delete_one(self, **kwargs):
        """
        Delete single document
        """
        self.write_cursor.delete_one(kwargs)

    def delete_many(self, **kwargs):
        """
        Delete multiple documents
        """
        self.write_cursor.delete_many(kwargs)
