from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewLoanBook(forms.Form):
    renewal_date = forms.DateField(help_text="Enter the date between now and 4 week (default: 3).")

    def clean_renewal_data(self):

        data = self.cleaned_data['renewal_date']

        #To check the entered renewal_date is lessthan current date, if so then raise an approriate error.
        if data < datetime.date.today():
            raise ValidationError(_("Renewal date is in Past."))

        #To check the entered renewal_date is not more than 4 weeks ahead, if so then raise an approriate error
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - as date is more than 4 weeeks ahead."))

        return data