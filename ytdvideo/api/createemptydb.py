from django.db import connections


def create_or_get_db():
    _id, _full_name = None, None
    with connections['admin'].cursor() as cursor:
        sql = """SELECT datname FROM pg_database where datname = {}""".format("'youtubevideos'")

        cursor.execute(sql)
        if not cursor.fetchall():
            sql = """CREATE DATABASE {}""".format("'youtubevideos'")
            cursor.execute(sql)
