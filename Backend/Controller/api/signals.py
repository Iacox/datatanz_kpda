import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from Config.settings import MEDIA_ROOT
from .models import RawFile
from .services.tasks import convert_file

@receiver(post_save, sender=RawFile)
def post_save_raw_file(sender, instance, created, **kwargs):
    if created:
        raw_file = RawFile.objects.get(pk = instance.pk)
        raw_file.status = False
        raw_file.save()
        file_path = str(raw_file.file_object).split('/')[-1]
        file_path = os.path.join(MEDIA_ROOT, 'input_files/' + file_path)
        file_pk = raw_file.pk

        convert_file.delay(file_path,file_pk)
