from django.urls import path
from .views import *


urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('warehouse', Warehouse_view.as_view(), name='warehouse'),
    path('report', Report.as_view(), name='report'),
]