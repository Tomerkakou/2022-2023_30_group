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
from worker.views import menu,inventory_receipt,showInventory ,showProduct,productSearch,showOrders,watchOrder,showReturns,inventory_To_Excel_for_worker,reports_for_worker,stocktaking_To_Excel,order_to_excel_for_worker
from website.views import start,log_out

urlpatterns = [
    path('',start,name='login'),
    path('logout/',log_out,name='logout'),
    path('',include('website.urls')),
    path('worker/menu/',menu,name='Worker_menu'),
    path('worker/menu/new_inventory/',inventory_receipt,name='newinventory'),
    path('worker/menu/inventory/',showInventory,name='showinventory'),
    path('worker/menu/Products/',productSearch,name='searchroduct'),
    path('worker/menu/Products/<int:id>/',showProduct,name='showproduct'),
    path('worker/menu/orders/',showOrders,name='ordersW'),
    path('worker/menu/returns/',showReturns,name='returns'),
    path('worker/menu/reports/',reports_for_worker,name='reports_worker'),
    path('inventory-worker-excel',inventory_To_Excel_for_worker,name='inventory-worker-excel') ,
    path('stocktaking-worker-excel',stocktaking_To_Excel,name='stocktaking-worker-excel') ,
    path('order_to_excel_for_worker/<int:order_id>/',order_to_excel_for_worker,name='order_to_excel_for_worker'),
    path('worker/menu/orders/<int:order_id>/',watchOrder,name='watchorderW'),


]