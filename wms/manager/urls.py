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
from django.urls import path,include
from manager.views import menu ,newProduct , newLocation,showUsers,createuser,showInventory,inventoryToExel,reports,report_entry_products
from website.views import start
urlpatterns = [
    path('',start,name='login'),
    path('',include('website.urls')),
    path('manager/menu/',menu,name='Manager_menu'),
    path('manager/menu/newProduct/',newProduct,name='newproduct'),
    path('manager/menu/newLocation/',newLocation,name='newlocation'),
    path('manager/menu/Users/',showUsers,name='showusers'),
    path('manager/menu/createUser/',createuser,name='createuser'),
    path('manager/menu/Inventory/',showInventory,name='Inventory'),
    path('manager/menu/reports/',reports,name='reports_manager'),
    path('inventory-exel',inventoryToExel,name='inventory-exel'),
    path('report_entry_products',report_entry_products,name='report_entry_products'),

]
