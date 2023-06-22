from django.urls import path
from .views import *

urlpatterns = [
    path('',recipe , name="recipe" ),
    path('delete/<int:id>/', deleteRecipe, name='delete'),
    path('update/<int:id>/', updateRecipe , name='update'),
    path('table/' , UserTable , name='table'),
    path('mailmodal/<int:cid>/' ,get_user_email , name='mailmodal'),
    path('userOrder/<int:uid>/', user_order , name='userOrder'),
    path('approval/<int:oid>/' , approval , name ='approval'),
]
