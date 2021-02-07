from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel


class VideoThumbnail(TimeStampedModel):
    DEFAULT = "default"
    MEDIUM = "medium"
    HIGH = "high"

    TYPE_CHOICES = Choices(
        (DEFAULT, DEFAULT, "DEFAULT TYPE"),
        (MEDIUM, MEDIUM, "MEDIUM TYPE"),
        (HIGH, HIGH, "HIGH TYPE"),
    )

    video = models.ForeignKey(
        "api.video",
        on_delete=models.CASCADE,
        related_name="get_thumbnails"
    )

    width = models.IntegerField("Width of Thumbnail")
    height = models.IntegerField("Height of Thumbnail")
    url = models.URLField(max_length=500)

    type = models.CharField(
        choices=TYPE_CHOICES,
        max_length=50,
        db_index=True
    )
