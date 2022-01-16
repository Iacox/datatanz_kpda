import os

from django.db import models
from pyasn1.compat.octets import null


class ProcessedFile(models.Model):
    file_object = models.FileField('File Object', upload_to='output_files')
    def filename(self):
        return os.path.basename(self.file_object.name)



class RawFile(models.Model):
    file_object = models.FileField('File Object',upload_to='input_files')
    status = models.BooleanField('Status', default=False)
    dpi = models.IntegerField('DPI',default=None, blank = True, null=True)
    processed_file = models.ForeignKey(ProcessedFile,
                                       verbose_name='processed_file',
                                       null=True,
                                       blank=True,
                                       on_delete=models.SET_NULL)

    def filename(self):
        return os.path.basename(self.file_object.name)

