from django.urls import path
from .views import *


urlpatterns = [
    path('', Incoming.as_view(), name='common'),
]

