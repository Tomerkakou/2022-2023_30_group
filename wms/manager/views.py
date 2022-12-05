from django.shortcuts import render, HttpResponse, redirect
from django.forms import modelform_factory
from website.models import products,locations,user
import manager.function

def menu(request):
    return render(request,"manager/menu.html",{"msg":request.COOKIES['user']})


product_form =modelform_factory(products,exclude=[])

def newProduct(request):
    if request.method == "POST" :
        form=product_form(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('menu')
        else:
            return render(request,"manager/new_product.html",{"form":form})
    else:
        form=product_form()
        return render(request,"manager/new_product.html",{"form":form})


location_form=modelform_factory(locations,exclude=[])

def newLocation(request):
    if request.method == "POST" :
        form=location_form(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('menu')
        else:
            return render(request,"manager/new_location.html",{"form":form})
    else:
        form=location_form()
        return render(request,"manager/new_location.html",{"form":form})


def showUsers(request):
    users=None
    if request.method == "POST":
        data=request.POST.dict()
        if 'search' in request.POST:
            return render(request,"manager/showusers.html",{"users":manager.function.getUsers(data),"u":data['username'],"f":data['fullname'],"e":data['email'],"r":data['role']})
        else:
            manager.function.deleteUser(list(data)[5])
            return render(request,"manager/showusers.html",{"users":manager.function.getUsers(data),"u":data['username'],"f":data['fullname'],"e":data['email'],"r":data['role']})    
    else:
        return render(request,"manager/showusers.html",{"users":users})
    

user_form=modelform_factory(user,exclude=['status'])


def createuser(request,msg=''):
    if request.method == "POST" :
        form=user_form(request.POST) 
        if form.is_valid():
            form.save()
            msg='User created successfully'
            return render(request,"manager/createuser.html",{"form":form,"message":msg})
        else:
            return render(request,"manager/createuser.html",{"form":form,"message":msg})
    else:
        form=user_form()
        return render(request,"manager/createuser.html",{"form":form,"message":msg})
