import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from random import randrange

from Sam import settings

from datetime import datetime
from django.core.management.base import BaseCommand
from requests_html import HTMLSession
from slugify import slugify

from newspaper.models import Image, News, Category, Tag


locker = Lock()


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    title = response.html.xpath("//h1")[0].text
    slug = slugify(title)
    text = "".join(('<p>{}</p>'.format(p.text) for p in response.html.xpath("//div[@class='entry-content']/p")[:-2]))
    published_at = response.html.xpath("//div[@class='single-meta']//span")[0].text[:-3]
    published_at = datetime.strptime(published_at, '%b %d, %Y')
    author = response.html.xpath("//div[@class='info']/a")[0].text

    categories_html_list = response.html.xpath("//ul[@class='post-categories']/li")
    categories = [category.text for category in categories_html_list]

    tags = response.html.xpath("//div[@class='single-tags']/a/text()")

    views = randrange(600, 900)
    rating = randrange(95, 230)

    news_data = {
        'title': title,
        'text': text,
        'news_source': url,
        'published_at': published_at,
        'author': author,
        'views': views,
        'rating': rating
    }

    try:
        with locker:
            news = News.objects.create(**news_data)
    except Exception as e:
        print(type(e), e)
        return

    for category in categories:
        with locker:
            category, created = Category.objects.get_or_create(name=category)
        news.category.add(category)

    for tag in tags:
        with locker:
            tag, created = Tag.objects.get_or_create(name=tag)
        news.tags.add(tag)

    news_img_dir = settings.BASE_DIR + '/media/news/' + news.slug

    if not os.path.exists(news_img_dir):
        os.makedirs(news_img_dir)

    image_sources = response.html.xpath("//div[@class='entry-content']//@src")

    with HTMLSession() as session2:

        for image_source in image_sources:

            img_resp = session2.get(image_source)
            image_name = image_source.rsplit(sep='/')[-1]

            with open(f'media/news/{slug}/{image_name}', 'wb') as img_file:
                img_file.write(img_resp.content)

            del img_resp

            try:
                with locker:
                    Image.objects.create(
                        news=news,
                        image='news/' + slug + '/' + image_name,
                        image_source=image_source
                    )

            except Exception as e:
                print(type(e), e)
                return

    print('Success ', url)


def urls_list(start, end):

    with HTMLSession() as session3:
        site_map = 'http://www.sci-news.com/post-sitemap7.xml'
        response2 = session3.get(site_map)
        urls = response2.html.xpath("//url/loc/text()")[start:end]

    return urls


def run_crawler(start, end, task):

    with locker:
        task.status = 'start parsing'
        task.save()
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(crawler, urls_list(start, end))
    with locker:
        task.status = 'finished'
        task.end_time = datetime.now()
        task.save()
    print('Done')


class Command(BaseCommand):

    help = 'Running news scraper'

    def handle(self, *args, **options):
        from task.models import Task
        task = Task.objects.create(name='run_scraper')
        run_crawler(1, 100, task)
        print('Done')
