import googleapiclient
import traceback

from rest_framework import exceptions
from googleapiclient.discovery import build
from youtubeapi.cachehandlers.youtubeapikeycachehandler import YouTubeAPIKeyCacheHandler
from youtubeapi.models import YoutubeVideoAPIKey


class YoutubeVideoSearchAdapter(object):
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    def get_developer_api_key(self):
        cache_handler = YouTubeAPIKeyCacheHandler()
        api_key = cache_handler.get_configuration()
        if not api_key:
            raise exceptions.NotFound("Active API Key Not Found")

    def youtube_search(self, search_term, max_results=100):
        api_key = None
        try:
            api_key = self.get_developer_api_key()
            print("using api key {}".format(api_key))
            youtube = build(
                self.YOUTUBE_API_SERVICE_NAME,
                self.YOUTUBE_API_VERSION,
                developerKey=api_key
            )

            search_response = youtube.search().list(
                q=search_term,
                part='id,snippet',
                maxResults=max_results,
                type="video",
                order="date",
                publishedAfter="2021-02-01T00:00:00Z",
            ).execute()

            videos = []
            for search_result in search_response.get('items', []):
                thumbnails_data = self.format_thumbnails_data(search_result['snippet']['thumbnails'])
                videos.append(
                    {
                        "title": search_result['snippet']['title'],
                        "description": search_result['snippet']['description'],
                        "video_id": search_result['id']['videoId'],
                        "published_at": search_result['snippet']['publishedAt'],
                        "thumbnails": thumbnails_data,
                    }
                )

            return videos
        except googleapiclient.errors.HttpError:
            print(traceback.format_exc())
            self.invalidate_api_key_cache(api_key)
            return []
        except exceptions.NotFound:
            print("Active API Key Not Found")
            return []

    def invalidate_api_key_cache(self, api_key):
        if api_key:
            YoutubeVideoAPIKey.objects.filter(
                key=api_key
            ).update(
                status=YoutubeVideoAPIKey.STATUS_CHOICES._identifier_map.get(YoutubeVideoAPIKey.INACTIVE)
            )
        cache_handler = YouTubeAPIKeyCacheHandler()
        cache_handler.invalidate_cache()
        cache_handler.get_configuration()

    def format_thumbnails_data(self, data={}):
        formatted_data = []
        for type, thumbnail_data in data.items():
            thumbnail_data["type"] = type
            formatted_data.append(thumbnail_data)

        return formatted_data
