from django.test import SimpleTestCase

from newspaper.forms import ReviewForm


class TestForm(SimpleTestCase):

    def test_expense_form_valid_data(self):
        form = ReviewForm(data={
            'name': 'review 1',
            'email': 'review@email.com',
            'web_site': 'some-web-site.com',
            'text': 'Some Text'
        })

        self.assertTrue(form.is_valid())

    def test_expense_form_no_data(self):
        form = ReviewForm(data={})

        self.assertFalse(form.is_valid())
