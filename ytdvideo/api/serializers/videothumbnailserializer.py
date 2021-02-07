from rest_framework import serializers
from api.models import VideoThumbnail


class VideoThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoThumbnail
        fields = '__all__'
