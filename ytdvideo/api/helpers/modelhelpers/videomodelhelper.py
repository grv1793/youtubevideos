from api.serializers.videoserializer import VideoSerializer


class VideoModelHelper(object):

    @staticmethod
    def get_obj_data(video):
        data = VideoSerializer(video).data
        return data
