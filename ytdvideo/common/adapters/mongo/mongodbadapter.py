import logging
import random

from django.conf import settings
from pymongo import MongoClient

from common.adapters.utils.singleton import Singleton

logger = logging.getLogger("vikas.event.log")


@Singleton
class MongoDBAdapter:
    def __init__(self, db_config_name):
        """write_clusters should contain one cluster or more clusters
        Whilst read_clusters can contain one or more than one cluster.
        Read up on master-slave architecture for more information.
        TLDR:
        - if there are multiple write clusters then you need to push the changes to each
        and every cluster.
        - We write to all of the master clusters and then can read from any of the multiple slave read clusters.
        The slaves are in sync with master.
        """
        self._write_clusters = []
        self._read_clusters = []
        self._all_clusters = []
        self.db_config_name = db_config_name

    def get_connection_url(self, host, port):
        return "mongodb://" + host + ":" + port

    @property
    def write_clusters(self):
        """Lazy implementation for fetching write clusters"""
        if self._write_clusters:
            return getattr(self, "_write_clusters")

        write_clusters_conf = settings.NOSQL_DATABASES[self.db_config_name][
            "write_clusters"
        ]

        self._write_clusters = []
        for write_cluster in write_clusters_conf:
            try:
                connection_url = self.get_connection_url(
                    write_cluster["host"], write_cluster["port"]
                )
                client = MongoClient(connection_url, serverSelectionTimeoutMS=1000)
                write_database = client[write_cluster['NAME']]
                if write_cluster.get('SHOULD_AUTHENTICATE', False):
                    write_database.authenticate(
                        write_cluster['USERNAME'],
                        write_cluster['PASSWORD'],
                        source=write_cluster['NAME'],
                        mechanism='SCRAM-SHA-1'
                    )
                self._write_clusters.append(write_database)
            except:
                logger.debug(
                    f"Error when initializing Mongo Write Cluster: {write_cluster}", exc_info=True
                )

        return self._write_clusters

    @property
    def read_clusters(self):
        """Lazy implementation for fetching read clusters"""
        if self._read_clusters:
            return getattr(self, "_read_clusters")

        read_clusters_conf = settings.NOSQL_DATABASES[self.db_config_name][
            "read_clusters"
        ]

        for read_cluster in read_clusters_conf:
            try:
                connection_url = self.get_connection_url(
                    read_cluster["host"], read_cluster["port"]
                )
                client = MongoClient(connection_url, serverSelectionTimeoutMS=1000)
                read_database = client[read_cluster['NAME']]

                if read_cluster.get('SHOULD_AUTHENTICATE', False):
                    read_database.authenticate(
                        read_cluster['USERNAME'],
                        read_cluster['PASSWORD'],
                        source=read_cluster['NAME'],
                        mechanism='SCRAM-SHA-1'
                    )

                self._read_clusters.append(read_database)
            except:
                logger.debug(
                    f"Error when initializing Mongo Read Cluster: {read_cluster}", exc_info=True
                )

        return self._read_clusters

    @property
    def all_clusters(self):
        if self._all_clusters:
            return getattr(self, "_all_clusters")
        return self.write_clusters + self.read_clusters

    def get_write_sessions(self):
        """Retrieve write session"""
        write_clusters = self.write_clusters
        if len(write_clusters) == 0:
            raise AssertionError("Write Cluster cannot be empty.")

        # TODO right now using only single write cluster in settings.
        return write_clusters[0]

    def get_read_session(self):
        """Retrive read session"""
        read_clusters = self.read_clusters
        if len(read_clusters) == 0:
            raise AssertionError("Read Cluster cannot be empty.")
        return random.choice(read_clusters)

    def get_all_sessions(self):
        all_clusters = self.all_clusters
        if len(all_clusters) == 0:
            raise AssertionError("No Cluster found.")

        return all_clusters
