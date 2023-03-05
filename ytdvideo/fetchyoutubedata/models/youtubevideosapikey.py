from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel


class YoutubeVideoAPIKey(TimeStampedModel):
    ACTIVE = "active"
    INACTIVE = "inactive"

    STATUS_CHOICES = Choices(
        (0, INACTIVE, "InActive"),
        (1, ACTIVE, "Active"),
    )

    key = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        db_index=True,
        default=STATUS_CHOICES._identifier_map.get(ACTIVE)
    )

