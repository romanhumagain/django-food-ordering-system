from django.urls import path
from .views import *

urlpatterns = [
  path('recipe/',recipe, name ='recipe'),
  
]
