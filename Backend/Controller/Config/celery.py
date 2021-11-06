import os

from celery import Celery
from kombu import Queue, Exchange

# Установка переменных окружения из django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')

# Инициализация приложения
app = Celery('Config')

# Использование настроек django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Установка очереди для рабочих Celery поумолчанию
app.conf.task_default_queue = 'default'

# Создание очередей для рабочих Celery
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('solo_task', Exchange('solo_task'), routing_key='solo_task'),
    Queue('ml_task', Exchange('ml_task'), routing_key='ml_task'),
    Queue('beat_task', Exchange('beat_task'), routing_key='beat_task'),
)

# Автоматический поиск задач
app.autodiscover_tasks(['api.services'])

# Создание расписания периодических задач для рабочих Celery
app.conf.beat_schedule = {
}
