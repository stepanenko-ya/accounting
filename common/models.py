from django.db import models


class IncomingInvoice(models.Model):
    items_data = models.ManyToManyField('IncomingItem', related_name='connection_items')
    time_create = models.DateField(auto_now_add=True)


class OutcomingInvoice(models.Model):
    items_data = models.ManyToManyField('OutcomingItem', related_name='connection_items')
    time_create = models.DateField(auto_now_add=True)


class IncomingItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name='Назва товару')
    quantity = models.IntegerField(verbose_name='Кількість')
    price = models.FloatField(verbose_name='Ціна закупівлі')
    warehouse = models.IntegerField(verbose_name='Залишок на складі')


class OutcomingItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name='Назва товару')
    quantity = models.IntegerField(verbose_name='Кількість')
    price = models.FloatField(verbose_name='Ціна продажу')
    profit = models.IntegerField(verbose_name='Прибуток')



class Item(models.Model):
    name = models.CharField(max_length=250)
    is_service = models.BooleanField(default=False)

    def __str__(self):
        return self.name











