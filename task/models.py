from django.db import models


class Task(models.Model):

    CHOICES = [
        ('run_scraper', 'Run Scraper'),
        ('count_images', 'Show Count Images')
    ]

    task = models.CharField(max_length=255, choices=CHOICES)
    status = models.CharField(max_length=255, null=True, blank=True)
    arg = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.task
