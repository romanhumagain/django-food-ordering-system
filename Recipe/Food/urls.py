from django.urls import path
from .views import *

urlpatterns = [
    path('',recipe , name="recipe" ),
    path('delete/<int:id>/', deleteRecipe, name='delete'),
    path('update/<int:id>/', updateRecipe , name='update'),
    path('table/' , UserTable , name='table'),
]
