from django.test import TestCase, Client, RequestFactory

from django.urls import reverse

from newspaper.models import News, Category
from newspaper.views import HomeView, SingleNewsView, CategoriesView


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.single_post_url = reverse('newspaper:single-post', kwargs={'slug': 'news1'})
        self.category_post_url = reverse('newspaper:categories-post', kwargs={'slug': 'category1'})
        self.contact_url = reverse('newspaper:contact')
        self.about_url = reverse('newspaper:about')

        self.news = News.objects.create(
            title='news1',
            text='some text',
            author='some author'
        )

        self.category = Category.objects.create(
            name='category1'
        )

    def test_single_post_GET(self):

        response = self.client.get(self.single_post_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'single-post.html')

    def test_category_post_GET(self):

        response = self.client.get(self.category_post_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories-post.html')

    def test_contact_GET(self):

        response = self.client.get(self.contact_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_about_GET(self):

        response = self.client.get(self.about_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_db_not_empty(self):
        news = News.objects.all()
        self.assertTrue(news)

    def test_home_page_context_obj_name(self):
        request = self.factory.get(reverse('newspaper:index'))
        home_obj = HomeView()
        home_obj.request = request
        context_obj_name = home_obj.context_object_name
        self.assertTrue(context_obj_name, 'news')

    def test_single_news_obj_exist(self):
        request = self.factory.get(reverse('newspaper:single-post', kwargs={'slug': self.news.slug}))
        single_news_obj = SingleNewsView()
        single_news_obj.request = request
        single_news_obj.kwargs = {'pk': self.news.pk}
        self.assertTrue(single_news_obj.get_object())

    def test_single_news_has_related_news(self):
        single_news_obj = SingleNewsView()
        single_news_obj.object = self.news
        request = self.factory.get(reverse('newspaper:single-post', kwargs={'slug': self.news.slug}))
        single_news_obj.request = request
        context = single_news_obj.get_context_data()
        self.assertIn('related_news', context)

    def test_news_by_category(self):
        category_news_obj = CategoriesView()
        category_news_obj.object = self.category
        request = self.factory.get(reverse('newspaper:categories-post', kwargs={'slug': self.category.slug}))
        self.news.category.add(self.category)
        self.news.save()
        category_news_obj.request = request
        self.assertTrue(category_news_obj.get_queryset())

    def test_category_obj(self):
        category_news_obj = CategoriesView()
        category_news_obj.object = self.category
        request = self.factory.get(reverse('newspaper:categories-post', kwargs={'slug': self.category.slug}))
        category_news_obj.request = request
        self.assertTrue(category_news_obj.object)
