from Config.celery import app as celery_app
from ..models import RawFile, ProcessedFile
from .recognizer.recognizer import recognizer


@celery_app.task(name='api.services.tasks.file_processing',
                 queue='ml_task',
                 routing_key='ml_task')
def file_processing(file_path: str):
    return recognizer(file_path)


@celery_app.task(name='api.services.tasks.save_processed_file',
                 queue='solo_task',
                 routing_key='solo_task')
def save_processed_file(file_path: str,file_pk: int):
    ProcessedFile.objects.create(file_object=file_path, pk=file_pk)


@celery_app.task(name='api.services.tasks.change_status',
                 queue='solo_task',
                 routing_key='solo_task')
def change_status(file_pk: int):
    raw_file = RawFile.objects.get(pk=file_pk)
    raw_file.status = True
    raw_file.save()


@celery_app.task(name='api.services.tasks.convert_file',
                 queue='default',
                 routing_key='default')
def convert_file(file_path: str, file_pk:int):
    (file_processing.s(file_path) | save_processed_file.s(file_pk) | change_status.si(file_pk))().forget()









