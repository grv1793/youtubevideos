from youtubeapi.adapters.youtubevideosearchadapter import YoutubeVideoSearchAdapter
from youtubeapi.configs.searchqueryterm import YTD_SEARCH_QUERY_TERMS


class SaveLatestVideosHelper(object):

    def save_videos_for_predefined_query_terms(self):
        for query_term in YTD_SEARCH_QUERY_TERMS:
            videos_result = self.get_video_data_from_query_term(query_term)
            self.save_videos_result(videos_result)

    def get_video_data_from_query_term(self, query_term):
        search_adapter = YoutubeVideoSearchAdapter()
        return search_adapter.youtube_search(query_term)

    def save_videos_result(self, videos_result):
        # TODO
        pass
