from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from newspaper.models import News, Category, Image, Tag, Review


class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 0
    exclude = ('image_source', )


class NewsAdmin(SummernoteModelAdmin):

    list_display = ('title', 'author', 'get_categories', 'published_at', 'views')
    inlines = [ImageAdmin]
    readonly_fields = ('slug', 'views', 'rating', 'news_source', 'published_at')
    fields = ('title', 'slug', 'author', 'text', 'category', 'tags', 'published_at', 'views', 'rating', 'news_source')
    summernote_fields = ('text', )

    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])

    get_categories.short_description = 'Categories'


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


class ReviewAdmin(SummernoteModelAdmin):
    list_display = ('name', 'published', 'moderated')
    list_editable = ('moderated', )
    summernote_fields = ('text', )


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Review, ReviewAdmin)
