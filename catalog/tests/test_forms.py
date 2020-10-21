import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewLoanBook

class RenewalBookFormTest(TestCase):

    def test_renewal_date_label(self):
        form = RenewLoanBook()
        self.assertTrue(form.fields['renewal_date'].label==None or
                    form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_help_text(self):
        form = RenewLoanBook()
        self.assertEqual(form.fields['renewal_date'].help_text,"Enter the date between now and 4 week (default: 3).")

    def test_renew_from_date_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewLoanBook(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
    def test_renew_date_to_future(self):
        date = datetime.date.today()+datetime.timedelta(weeks=4)+datetime.timedelta(days=1)
        form = RenewLoanBook(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
    def test_renew_date_today(self):
        date = datetime.date.today()
        form = RenewLoanBook(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
    def test_renew_date_max(self):
        date = datetime.date.today()+datetime.timedelta(weeks=4)
        form = RenewLoanBook(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
