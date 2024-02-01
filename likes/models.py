from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LikedItemManager(models.Manager):
    def do_like(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return LikedItem.objects.filter(content_type=content_type, object_id=obj_id)


class LikedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
