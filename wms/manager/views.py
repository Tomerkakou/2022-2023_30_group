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
            filter1=''
            filter2=''
            filter3=''
            filter4=''
            search=request.POST.dict()
            if search['username']!='':
                filter1=f"AND username='{search['username']}'"
            if search['fullname']!='':
                filter2=f"AND name='{search['fullname']}'"
            if search['email']!='':
                filter3=f"AND email='{search['email']}'"
            if search['role']!='':
                filter4=f"AND role='{search['role']}'"
            users=user.objects.raw(f"SELECT * FROM `website_user` WHERE status=1 {filter1} {filter2} {filter3} {filter4};")   
            return render(request,"manager/showusers.html",{"users":users})
        else:
            delete=user.objects.get(username=list(request.POST.dict())[1])
            delete.status=0
            delete.save()
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
