from django.contrib import admin

from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(IncomingInvoice)
class IncomingInvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(OutcomingInvoice)
class OutcomingInvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(IncomingItem)
class IncomingItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OutcomingItem)
class OutcomingItemAdmin(admin.ModelAdmin):
    pass