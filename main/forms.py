

from django import forms


class DateForm(forms.Form):
    start = forms.DateField()
    stop = forms.DateField()
