from datetime import datetime

from django.contrib.auth.models import User
from slugify import slugify
from django.db import models


class News(models.Model):

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    published_at = models.DateField()
    author = models.CharField(max_length=255)

    category = models.ManyToManyField('newspaper.Category')
    tags = models.ManyToManyField('newspaper.Tag')

    views = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)

    news_source = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.published_at:
            self.published_at = datetime.now()
        super(News, self).save(*args, **kwargs)


def image_folder(instance, filename):

    return "news/{0}/{1}".format(instance.news.slug, filename)


class Image(models.Model):

    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_folder)
    image_source = models.URLField(null=True, blank=True)


class Category(models.Model):

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Review(models.Model):

    name = models.CharField(max_length=255)
    published = models.DateTimeField(null=True, blank=True)
    text = models.TextField()
    moderated = models.BooleanField(default=False)

    email = models.EmailField()
    web_site = models.URLField()

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.moderated:
            self.published = datetime.now()
        return super().save()
