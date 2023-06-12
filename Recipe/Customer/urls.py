from django.urls import path
from Customer.views import *

urlpatterns = [
  path('dashboard/', customer_dashboard , name='dashboard' ),
]