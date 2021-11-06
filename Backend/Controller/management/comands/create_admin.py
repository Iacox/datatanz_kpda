from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from Config import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:
            for admin in settings.ADMINS:
                username, email, password = admin.values()
                User.objects.create_superuser(username=username,
                                              email=email,
                                              password=password)
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
