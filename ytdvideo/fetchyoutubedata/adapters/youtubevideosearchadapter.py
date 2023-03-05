import traceback

from googleapiclient.discovery import build
from rest_framework import exceptions

from fetchyoutubedata.cachehandlers.youtubeapikeycachehandler import YouTubeAPIKeyCacheHandler
from fetchyoutubedata.models import YoutubeVideoAPIKey


class YoutubeVideoSearchAdapter(object):
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    
    def __init__(self, published_after, published_before):
        self.published_after = published_after
        self.published_before = published_before
        self.api_key = self.get_api_key()
        self.data = []

    def youtube_search(self, search_term, max_results=50):
        if self.api_key:
            is_success = True
            try:
                search_response = self.make_api_call_to_youtube(search_term, max_results)
                self.data = self.format_search_response(search_response)
            except:
                is_success = False
                print(traceback.format_exc())
                self.invalidate_api_key_cache()
        else:
            print("Active API Key Not Found")
            is_success = False

        return is_success, self.data

    def make_api_call_to_youtube(self, search_term, max_results):
        print("using api key {}".format(self.api_key))
        youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.api_key
        )

        return youtube.search().list(
            q=search_term,
            part='id,snippet',
            maxResults=max_results,
            type="video",
            order="date",
            publishedAfter=self.published_after,
            publishedBefore=self.published_before,
        ).execute()

    def format_search_response(self, search_response):
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

    def get_api_key(self):
        cache_handler = YouTubeAPIKeyCacheHandler()
        return cache_handler.get_configuration()

    def invalidate_api_key_cache(self):
        if self.api_key:
            YoutubeVideoAPIKey.objects.filter(
                key=self.api_key
            ).update(
                status=YoutubeVideoAPIKey.STATUS_CHOICES._identifier_map.get(YoutubeVideoAPIKey.INACTIVE)
            )
        cache_handler = YouTubeAPIKeyCacheHandler()
        cache_handler.invalidate_cache()
        cache_handler.get_configuration()

    def format_thumbnails_data(self, data=None):
        if data is None:
            data = {}

        formatted_data = []
        for thumbnail_type, thumbnail_data in data.items():
            thumbnail_data["type"] = thumbnail_type
            formatted_data.append(thumbnail_data)

        return formatted_data
