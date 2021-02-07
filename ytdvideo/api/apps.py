from django.apps import AppConfig
from api.createemptydb import create_or_get_db


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        """ INIT """
        print("Init ApiConfig")
        create_or_get_db()
        print("executed create_or_get_db")
