from django.test import TestCase

from newspaper.models import News, Category, Tag


class TestModels(TestCase):

    def setUp(self):
        self.news = News.objects.create(
            title='news 1',
            text='some text',
            author='some author'
        )
        self.category = Category.objects.create(
            name='category 1'
        )
        self.tag = Tag.objects.create(
            name='tag 1',
        )

    def test_news_is_assigned_slug_on_creation(self):
        self.assertEquals(self.news.slug, 'news-1')

    def test_category_is_assigned_slug_on_creation(self):
        self.assertEquals(self.category.slug, 'category-1')

    def test_tag_is_assigned_slug_on_creation(self):
        self.assertEquals(self.tag.slug, 'tag-1')
