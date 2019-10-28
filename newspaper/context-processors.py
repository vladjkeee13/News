from newspaper.models import Category, News


def filter_categories(request):

    categories = Category.objects.all()
    slugs_of_main_category = ['astronomy', 'space-exploration', 'archaeology', 'paleontology', 'biology', 'physics',
                              'medicine', 'genetics', 'geology']
    main_category = categories.filter(slug__in=slugs_of_main_category)

    context = {
        'categories': categories,
        'main_categories': main_category
    }
    return context


def filter_news(request):

    news = News.objects.all().prefetch_related('category')
    latest_news = news[:4]
    top_news = news.order_by('-views')[:4]

    context = {

        'latest_news': latest_news,
        'top_news': top_news
    }
    return context
