from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from catalog.models import PhoneNumber

class RenewLoanBook(forms.Form):
    renewal_date = forms.DateField(help_text="Enter the date between now and 4 week (default: 3).")
    def clean_renewal_date(self):

        data = self.cleaned_data['renewal_date']

        #To check the entered renewal_date is lessthan current date, if so then raise an approriate error.
        if data < datetime.date.today():
            raise ValidationError(_("Renewal date is in Past."))

        #To check the entered renewal_date is not more than 4 weeks ahead, if so then raise an approriate error
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - as date is more than 4 weeeks ahead."))
        return data

class UserRegister(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email','password1','password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class UserProfileDetails(forms.Form):
    firstname = forms.CharField()
    lastname = forms.CharField()

    def save(self):
        super.save(self)
