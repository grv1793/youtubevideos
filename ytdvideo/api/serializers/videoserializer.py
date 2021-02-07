from django.db import transaction

from rest_framework import serializers

from api.models import Video
from api.serializers.videothumbnailserializer import VideoThumbnailSerializer
from api.signals.video import video_post_save_signal


class VideoSerializer(serializers.ModelSerializer):
    thumbnails = VideoThumbnailSerializer(required=False, many=True)

    def create(self, validated_data):
        with transaction.atomic():
            thumbnails_data = validated_data.pop("thumbnails")
            video = Video(**validated_data)
            video.save()

            for thumbnail_data in thumbnails_data:
                ser = VideoThumbnailSerializer(data=thumbnail_data)
                ser.is_valid(raise_exception=True)
                video_thumbnail = ser.save()
                video.thumbnails.add(video_thumbnail)

            video_post_save_signal(video, True)
            return video

    class Meta:
        model = Video
        fields = '__all__'
