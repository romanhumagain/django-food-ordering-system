from django.urls import path
from Customer.views import *

urlpatterns = [
  path('' , home , name ='home'),
  path('dashboard/<int:id>/', customer_dashboard , name='dashboard'),
  path('orderhistory/<int:cid>/' ,OrderHistory , name = 'orderhistory'),
  path('order/<int:cid>/<int:id>/' , customer_order , name='order'),
  path('deleteOrder/<int:id>/', deleteOrder, name='deleteOrder'),
  path('updateOrder/<int:cid>/<int:id>/' , updateOrder , name='updateOrder'),
  path('logout/' , logout_account , name = 'logout' ),
  path('mail/' , sendMail , name='mail'),
]