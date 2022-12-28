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
from student.views import menu,showInventory,watchOrder,showOrders,products_To_Excel_for_student,reports,recepit,price_To_Excel
from website.views import start


urlpatterns = [
    path('',start,name='login'),
    path('',include('website.urls')),
    path('student/menu/',menu,name='Student_menu'),
    path('student/menu/inventory',showInventory,name='inventory'),
    path('student/menu/orders/<int:order_id>/',watchOrder,name='watchorder'),
    path('student/menu/orders',showOrders,name='orders'),
    path('student/menu/reports/',reports,name='reports_student'),
    path('products-student-exel',products_To_Excel_for_student,name='products-student-exel'),
    path('Receipt-<int:order_id>',recepit,name='receipt'), 
    path('price-student-exel',price_To_Excel,name='price-student-exel'), 
]

