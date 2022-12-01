from django.shortcuts import render, HttpResponse, redirect
from django.forms import modelform_factory
from website.models import products,locations,user

def menu(request):
    return render(request,"manager/menu.html")
# Create your views here.

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
        if 'search' in request.POST:
            search=request.POST.dict()
            users=user.objects.filter(status=1)
            u_list=list()
            for i in users:
                flag=1
                if search['username']!='' and str(i.username)!=search['username']:
                    flag=0
                if search['fullname']!='' and str(i.name)!=search['name']:
                    flag=0
                if search['email']!='' and str(i.email)!=search['email']:
                    flag=0
                if search['role']!='' and str(i.role)!=search['role']:
                    flag=0
                if flag==1:
                    u_list.append(i)
            return render(request,"manager/showusers.html",{"users":u_list})
        else:
            for i in user.objects.all() :
                if str(i.username) in request.POST:
                    i.status=0
                    i.save()
            return render(request,"manager/showusers.html",{"users":users})    
    else:
        return render(request,"manager/showusers.html",{"users":users})
    

user_form=modelform_factory(user,exclude=['status'])


def createuser(request,msg=''):
    if request.method == "POST" :
        form=user_form(request.POST) 
        if form.is_valid():
            form.save()
            msg='User successfully created'
            return render(request,"manager/createuser.html",{"form":form,"message":msg})
        else:
            return render(request,"manager/createuser.html",{"form":form,"message":msg})
    else:
        form=user_form()
        return render(request,"manager/createuser.html",{"form":form,"message":msg})
