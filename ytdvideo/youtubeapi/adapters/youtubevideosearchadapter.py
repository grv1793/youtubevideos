import random
import traceback
from googleapiclient.discovery import build


class YoutubeVideoSearchAdapter(object):
    DEVELOPER_KEYS = [
        'AIzaSyBH3iPE5gWydu22guG41x7yIchbYav8VJM',
    ]
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    def get_developer_api_key(self):
        # TODO use new key only when previous key expires
        # check response of api if key quota is reached and then fetch new api key
        return random.choice(self.DEVELOPER_KEYS)

    def youtube_search(self, search_term, max_results=100):
        try:
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
        except:
            print(traceback.format_exc())
            pass

    def format_thumbnails_data(self, data={}):
        formatted_data = []
        for type, thumbnail_data in data.items():
            thumbnail_data["type"] = type
            formatted_data.append(thumbnail_data)

        return formatted_data
