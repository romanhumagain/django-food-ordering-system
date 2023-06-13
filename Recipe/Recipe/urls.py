"""
URL configuration for Recipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Food.views import *
from Customer.views import *
from Food import urls
from Customer import urls
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , home , name ='home'),
    path('login/', login , name='login'),
    path('register/', register , name='register'),
    path('logout/', logout_page , name='logout'),
    path('recipe/',recipe , name="recipe" ),
    path('delete/<int:id>/', deleteRecipe, name='delete'),
    path('update/<int:id>/', updateRecipe , name='update'),
    path('table/' , UserTable , name='table'),
    path('dashboard/<int:id>/', customer_dashboard , name='dashboard'),
    path('orderhistory/<int:cid>/' ,OrderHistory , name = 'orderhistory'),
    path('order/<int:cid>/<int:id>/' , customer_order , name='order'),
    path('deleteOrder/<int:id>/', deleteOrder, name='deleteOrder'),
    path('updateOrder/<int:cid>/<int:id>/' , updateOrder , name='updateOrder'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

