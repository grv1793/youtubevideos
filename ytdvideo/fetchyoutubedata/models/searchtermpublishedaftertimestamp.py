from django.db import models
from model_utils.models import TimeStampedModel


class SearchTermPublishedAfterTimestamp(TimeStampedModel):
    published_after = models.DateTimeField(db_index=True)
    search_term = models.CharField(
        max_length=250,
        db_index=True,
    )
