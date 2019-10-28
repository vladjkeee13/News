import logging

from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages

from newspaper.models import Category, News, Review
from newspaper.forms import ReviewForm


logger = logging.getLogger('django')


class HomeView(ListView):
    template_name = 'index.html'
    model = News
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        logger.debug(context)
        return context


class SingleNewsView(DetailView):
    template_name = 'single-post.html'
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        related_news = News.objects.filter(category=self.object.category.first()).exclude(slug=self.object.slug)[:2].prefetch_related('category')
        reviews = Review.objects.filter(news=self.object, moderated=True)
        context['related_news'] = related_news
        context['reviews'] = reviews
        return context

    def post(self, *args, **kwargs):

        self.object = self.get_object()

        form = ReviewForm(self.request.POST)

        if form.is_valid():
            form.save(news=self.object)
            messages.add_message(self.request, messages.INFO, 'Thanks! Your review is on moderation.')
            return redirect('newspaper:single-post', slug=self.object.slug)
        else:
            logger.warning(form)
            messages.add_message(self.request, messages.INFO, 'Incorrect data')
            context = self.get_context_data()
            context['form'] = form

        return self.render_to_response(context)


class CategoriesView(SingleObjectMixin, ListView):
    template_name = 'categories-post.html'
    paginate_by = 7

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context

    def get_queryset(self):
        return self.object.news_set.all().prefetch_related('category')


class SearchView(ListView):
    template_name = 'categories-post.html'
    paginate_by = 7

    def get_queryset(self):
        search_text = self.request.GET.get('search')
        if search_text:
            return News.objects.filter(title__contains=search_text)
        else:
            return News.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        search_text = self.request.GET.get('search')
        context['search_text'] = search_text
        return context


class AboutUsView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'
