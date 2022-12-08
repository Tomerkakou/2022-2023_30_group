"""wms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from worker.views import menu,inventory_receipt,showInventory ,showProduct,productSearch
from website.views import start

urlpatterns = [
    path('',start,name='login'),
    path('worker/menu/',menu,name='menu'),
    path('worker/menu/new_inventory/',inventory_receipt,name='newinventory'),
    path('worker/menu/inventory/',showInventory,name='showinventory'),
    path('worker/menu/Products/',productSearch,name='searchroduct'),
    path('worker/menu/<int:id>/',showProduct,name='showproduct'),
]