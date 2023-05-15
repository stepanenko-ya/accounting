from django import forms


class SaleForm(forms.Form):
    invoice_number = forms.CharField(max_length=300)
    item = forms.CharField(label='Назва товару')
    price = forms.FloatField(label='Ціна за одиницю товару')
    quantity = forms.IntegerField(label='Кількість', required=True)
