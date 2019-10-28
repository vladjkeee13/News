from django.test import SimpleTestCase
from django.urls import reverse, resolve

from newspaper.views import HomeView, SingleNewsView, CategoriesView, AboutUsView, ContactView, SearchView


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('newspaper:index')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_single_post_url_resolves(self):
        url = reverse('newspaper:single-post', kwargs={'slug': 'some-slug'})
        self.assertEqual(resolve(url).func.view_class, SingleNewsView)

    def test_categories_post_url_resolves(self):
        url = reverse('newspaper:categories-post', kwargs={'slug': 'some-slug'})
        self.assertEqual(resolve(url).func.view_class, CategoriesView)

    def test_about_url_resolves(self):
        url = reverse('newspaper:about')
        self.assertEqual(resolve(url).func.view_class, AboutUsView)

    def test_contact_url_resolves(self):
        url = reverse('newspaper:contact')
        self.assertEqual(resolve(url).func.view_class, ContactView)

    def test_search_url_resolves(self):
        url = reverse('newspaper:search')
        self.assertEqual(resolve(url).func.view_class, SearchView)
