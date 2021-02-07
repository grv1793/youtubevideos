from django.db import models
from model_utils.models import TimeStampedModel


class VideoThumbnail(TimeStampedModel):

    video = models.ForeignKey(
        'api.video',
        on_delete=models.CASCADE,
        related_name="get_thumbnails"
    )

    width = models.IntegerField('Width of Thumbnail')
    height = models.IntegerField('Height of Thumbnail')
    field_name = models.URLField(max_length=500)
