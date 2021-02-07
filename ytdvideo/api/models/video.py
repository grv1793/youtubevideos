from django.db import models
from model_utils.models import TimeStampedModel


class Video(TimeStampedModel):

    video_id = models.CharField(max_length=100, unique=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(db_index=True)
