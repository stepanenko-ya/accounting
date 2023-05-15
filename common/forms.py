from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import modelformset_factory


class ArrivedForm(forms.Form):
    invoice_number = forms.CharField(max_length=300)
    item = forms.CharField(label='Назва товару')
    quantity = forms.IntegerField(label='Кількість', required=True)
    price = forms.FloatField(label='Ціна за одиницю товару')





