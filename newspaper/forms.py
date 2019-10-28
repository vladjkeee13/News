from django.forms import ModelForm
from newspaper.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'web_site', 'text']

    def save(self, *args, **kwargs):
        review = super().save(commit=False)
        review.news = kwargs.get('news')
        review.save()
        return review
