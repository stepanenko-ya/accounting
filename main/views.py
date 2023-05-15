from datetime import datetime

from django.shortcuts import render
from django.views.generic import DetailView
from common.models import *
from django.db.models import Prefetch
from django.db.models import Sum
from .forms import DateForm

class Main(DetailView):
    context = {'title': 'Головна сторінка'}

    def get(self, request, *, object_list=None, **kwargs):
        return render(request, "main/main.html", context)


class Warehouse_view(DetailView):

    def get(self, request, *, object_list=None, **kwargs):
        context = {'title': 'Склад товарів'}
        return render(request, "main/warehouse.html", context)

    def post(self, request, *args, **kwargs):
        context = {'title': 'Склад товарів'}
        orders_outcoming = {}
        orders_incoming = {}
        item_set = set()
        result = {}
        if request.method == 'POST':
            form = DateForm(request.POST)
            start = dict(form.data.items()).get('date_start')
            if not start:
                context['error'] = 'Зазначена дата не коректна'
                return render(request, "main/warehouse.html", context)

            for i in IncomingInvoice.objects.filter(time_create__lte=start).prefetch_related(Prefetch('items_data')):
                for el in i.items_data.all():
                    item_name = el.item.name
                    if not el.item.is_service:
                        item_set.add(item_name)
                        orders_incoming.setdefault(item_name, 0)
                        orders_incoming[item_name] += el.quantity

            for i in OutcomingInvoice.objects.filter(time_create__lte=start).prefetch_related(Prefetch('items_data')):
                for el in i.items_data.all():
                    item_name = el.item.name
                    if not el.item.is_service:
                        item_set.add(item_name)
                        orders_outcoming.setdefault(item_name, 0)
                        orders_outcoming[item_name] += el.quantity

            for el_set in item_set:
                try:
                    res = orders_incoming.get(el_set) - orders_outcoming.get(el_set)
                except:
                    res = orders_incoming.get(el_set)
                result[el_set] = res
            context["results"] = result
            context["table_name"] = f"Склад товарів на {start}"
            return render(request, "main/warehouse.html", context)


class Report(DetailView):

    def get(self, request, *, object_list=None, **kwargs):
        context = {'title': 'Звіт'}
        # orders = {}
        # queryset = Invoice.objects.prefetch_related(Prefetch('items_data'))
        # for i in queryset.filter(status='loss'):
        #     for el in i.items_data.all():
        #         item_name = el.item.name
        #         if not el.item.is_service:
        #             orders.setdefault(item_name, {'quantity': 0})
        #             orders[item_name]["quantity"] += el.quantity
        #             orders[item_name]["price"] = el.price
        # for element_orders in orders:
        #     orders[element_orders]['total'] = orders[element_orders]['quantity'] * orders[element_orders]['price']
        #
        # self.context['result'] = orders
        # self.context['report'] = 'Звіт за весь період'

        return render(request, "main/report.html", context)

    def post(self, request, *args, **kwargs):
        context = {'title': 'Звіт'}
        result = {}
        if request.method == 'POST':
            form = DateForm(request.POST)
            start = dict(form.data.items()).get('date_start')
            stop = dict(form.data.items()).get('date_stop')
            if not start or not stop:
                context['error'] = 'Зазначена дата не коректна'
                return render(request, "main/report.html", context)

            invoices = OutcomingInvoice.objects.filter(time_create__range=[start, stop]).prefetch_related(Prefetch('items_data'))
            for items in invoices:
                for el in items.items_data.all():
                    if not el.item.is_service:
                        item_name = el.item.name
                        result.setdefault(item_name, {"quantity": 0, "profit": 0})
                        if not el.item.is_service:
                            result[item_name]["quantity"] += el.quantity
                            result[item_name]["profit"] += el.profit
            context['result'] = result
            context['report'] = f'Звіт за період {start} - {stop}'
            return render(request, "main/report.html", context)

