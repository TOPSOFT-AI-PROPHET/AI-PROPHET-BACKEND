from django.db import models
import uuid

# Create your models here.
class File(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=1025, verbose_name='file name')
    file_bin = models.BinaryField()
    file_uuid = models.UUIDField(default=uuid.uuid4, unique=True)