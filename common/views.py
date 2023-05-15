import os
from django.shortcuts import render
from django.views.generic import DetailView, View
from django.views.generic.edit import FormView
from .forms import ArrivedForm
from .models import *


class Incoming(DetailView):
    template_name = 'arrival/arrival.html'
    form_class = ArrivedForm
    context = {'title': 'Прибуткова накладна'}

    def get(self, request, *, object_list=None, **kwargs):
        self.context['form'] = ArrivedForm()
        self.context['items'] = Item.objects.all()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            form = self.form_class(request.POST)
            item_list = form.data.getlist("item")
            price_list = form.data.getlist("price")
            quantity_list = form.data.getlist("newQuantityInput")
            data_connection_items = []
            for item_block in list(zip(item_list, price_list, quantity_list)):
                current_item = Item.objects.get(name=item_block[0])
                arrived_data = IncomingItem.objects.create(
                    item=current_item,
                    price=item_block[1],
                    quantity=item_block[2],
                    warehouse=item_block[2])
                data_connection_items.append(arrived_data)

            invoice = IncomingInvoice.objects.create()
            invoice.items_data.set(data_connection_items)

            context['message'] = f'Прибуткова накладна № {invoice.id} створенна успішно'
            return render(request, 'arrival/arrival.html', context)



