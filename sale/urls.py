from django.urls import path
from .views import *


urlpatterns = [
    path('', Outcoming.as_view(), name='sale'),
]
