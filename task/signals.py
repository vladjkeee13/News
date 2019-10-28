from django.db.models.signals import post_save
from threading import Thread

from newspaper.management.commands.get_news import run_crawler
from newspaper.models import Image
from task.models import Task


def handler_run_scraper(sender, instance, **kwargs):
    if kwargs.get('created'):
        if instance.task == 'run_scraper':
            try:
                start, end = instance.arg.split(',')
                start, end = int(start), int(end)
            except Exception as e:
                print(e, type(e))
                start, end = 0, 100
            Thread(target=run_crawler, args=(start, end, instance)).start()
        elif instance.task == 'count_images':
            instance.status = f'images: {Image.objects.count()}'
            instance.save()


post_save.connect(handler_run_scraper, sender=Task)
