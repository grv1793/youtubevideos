import random

from googleapiclient.discovery import build


class YoutubeVideoSearchAdapter(object):
    DEVELOPER_KEYS = [
        'AIzaSyC2O5MHED-CE9in60bDi5c_1DSFK5__7Nc',
        'AIzaSyDVpLRy5PHZRXR44InVfmvMQpWNerC48PA',
        'AIzaSyAoNtsYSorx4P9x5nLnhWBU5YJQ3uBiIMU',
        'AIzaSyD6p3X1Tlk0oKdG-ZRYb6RRTIKygK6-oIk',
    ]
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    def get_developer_api_key(self):
        return random.choice(self.DEVELOPER_KEYS)

    def youtube_search(self, search_term, max_results=10):
        youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.get_developer_api_key()
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
            videos.append(
                {
                    "title": search_result['snippet']['title'],
                    "description": search_result['snippet']['publishedAt'],
                    "id": search_result['id']['videoId'],
                    "published_at": search_result['snippet']['publishedAt'],
                }
            )

        return videos
