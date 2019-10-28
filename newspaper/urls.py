from django.urls import path

from newspaper.views import HomeView, SingleNewsView, CategoriesView, AboutUsView, ContactView, SearchView

app_name = 'newspaper'

urlpatterns = [
    path('index/', HomeView.as_view(), name='index'),
    path('single-post/<slug:slug>', SingleNewsView.as_view(), name='single-post'),
    path('categories_post/<slug:slug>', CategoriesView.as_view(), name='categories-post'),
    path('about/', AboutUsView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('search/', SearchView.as_view(), name='search'),
]
