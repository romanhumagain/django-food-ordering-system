from django.urls import path
from .views import *

urlpatterns = [
  path('' , home , name ='home'),
  path('login/', login , name='login'),
  path('register/', register , name='register'),
  path('logout/', logout_page , name='logout'),
  path('recipe/',recipe , name="recipe" ),
]
