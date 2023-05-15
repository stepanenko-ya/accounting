import os
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import DetailView, View
from django.views.generic.edit import FormView
from .forms import SaleForm
from django.db.models import Sum
from common.models import *


class Outcoming(DetailView):
    template_name = 'sale/sale.html'


    @staticmethod
    def check_warehouse(out_data):
        insufficient = {}
        for item_block in out_data:
            if item_block[0] !='Доставка':
                current_item = Item.objects.get(name=item_block[0])

                count_items = IncomingItem.objects.filter(item=current_item).aggregate(res=Sum('warehouse'))['res']
                if count_items >= int(item_block[2]):
                    pass
                else:
                    insufficient[current_item.name] = count_items-int(item_block[2])
        return insufficient


    def get(self, request, *, object_list=None, **kwargs):
        context = {'title': 'Видаткова накладна'}
        context['items'] = Item.objects.all()
        return render(request, "sale/sale.html", context)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            context = {'title': 'Видаткова накладна'}
            data_connection_items = []
            form = SaleForm(request.POST)
            item_list = form.data.getlist("item")
            price_list = form.data.getlist("price")
            quantity_list = form.data.getlist("newQuantityInput")
            out_data = list(zip(item_list, price_list, quantity_list))


            enough_count = self.check_warehouse(out_data)

            if len(enough_count) > 0:
                error_list = [(el[0], abs(el[1])) for el in list(enough_count.items())]
                context['errors'] = error_list
                context['items'] = Item.objects.all()
                return render(request, 'sale/sale.html', context)

            # if not all(enough_count):
            #     context['error'] = f"Данна кілкость товарів недоступна на складі"
            #     context['items'] = Item.objects.all()
            #     return render(request, 'sale/sale.html', context)
            #
            #
            incoming_instance = IncomingItem.objects.all()
            for element_data in out_data:
                item_name = element_data[0]

                sale_price = float(element_data[1])
                sale_quantity = int(element_data[2])
                total_quantity = sale_quantity
                profit = []
                for el_instance in incoming_instance.filter(item__name=item_name):

                    if el_instance.warehouse >= total_quantity:
                        el_instance.warehouse -= total_quantity
                        profit.append((sale_price - el_instance.price)*total_quantity)

                        el_instance.save()
                        break
                    else:
                        total_quantity = total_quantity - el_instance.warehouse
                        profit.append((sale_price - el_instance.price)*el_instance.warehouse)
                        el_instance.warehouse = 0
                        el_instance.save()

                out_coming_data = OutcomingItem.objects.create(
                    item=Item.objects.get(name=item_name),
                    price=sale_price,
                    quantity=sale_quantity,
                    profit=sum(profit))

                data_connection_items.append(out_coming_data)
            outcoming_invoice = OutcomingInvoice.objects.create()
            outcoming_invoice.items_data.set(data_connection_items)

            context['message'] = f'Видаткова накладна № {outcoming_invoice.id} створенна успішно'
            # return render(request, 'arrival/arrival.html', context)
            return render(request, self.template_name, context)



