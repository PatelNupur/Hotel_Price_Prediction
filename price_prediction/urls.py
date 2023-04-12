from django.urls import path
from .views import *

urlpatterns = [
    path('', price, name='price'),
    path('price_prediction', price_prediction, name='price_prediction'),
    path('rate', rate, name='rate'),
    path('rate_prediction', rate_prediction, name='rate_prediction'),
]
