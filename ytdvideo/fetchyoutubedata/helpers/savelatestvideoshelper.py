import traceback
from fetchyoutubedata.adapters.youtubevideosearchadapter import YoutubeVideoSearchAdapter
from fetchyoutubedata.configs.searchqueryterm import YTD_SEARCH_QUERY_TERMS
from fetchyoutubedata.helpers.fetchvideopublishedtimestampshelper import FetchVideoPublishedTimestampsHelper
from api.serializers.videoserializer import VideoSerializer


class SaveLatestVideosHelper(object):

    def save_videos_for_predefined_search_terms(self):
        for search_term in YTD_SEARCH_QUERY_TERMS:
            videos_result = self.get_video_data_from_search_term(search_term)
            self.save_videos_result(videos_result)

    def get_video_data_from_search_term(self, search_term):
        helper = FetchVideoPublishedTimestampsHelper(search_term)
        published_after = helper.get_published_after_timestamp()
        published_before = helper.get_published_before_timestamp()

        print("search_term", "published_after", "published_before")
        print(search_term, published_after, published_before)

        search_adapter = YoutubeVideoSearchAdapter(published_after, published_before)
        is_success, data = search_adapter.youtube_search(search_term)

        if is_success:
            helper.update_published_after_timestamp()

        return data

    def save_videos_result(self, videos_result):
        for result in videos_result:
            try:
                ser = VideoSerializer(data=result)
                ser.is_valid(raise_exception=True)
                ser.save()
            except:
                print(traceback.format_exc())
