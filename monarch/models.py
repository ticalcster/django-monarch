from django.contrib.contenttypes.generic import GenericForeignKey  # django 1.9 need to be .fields
from django.contrib.contenttypes.models import ContentType
from django.db import models

class RecordLink(models.Model):
    legacy_table = models.CharField(max_length="100")
    legacy_pk_field = models.CharField(max_length="100")
    legacy_pk_value = models.CharField(max_length="100")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ("legacy_table", "legacy_pk_field", "legacy_pk_value")
