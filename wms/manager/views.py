from django.shortcuts import render,HttpResponse
import manager.function
from manager.forms import productForm,locationForm,userForm
from website.models import user

def menu(request):
    return render(request,"manager/menu.html")

def newProduct(request):
    if request.method == "POST" :
        form=productForm(request.POST) 
        if form.is_valid():
            form.save()
            return render(request,"manager/new_product.html",{"form":form,"message":"New product created successfully"})
        else:
            return render(request,"manager/new_product.html",{"form":form})
    else:
        form=productForm()
        return render(request,"manager/new_product.html",{"form":form})


def newLocation(request):
    if request.method == "POST" :
        form=locationForm(request.POST) 
        if form.is_valid():
            form.save()
            return render(request,"manager/new_location.html",{"form":form,"message":"Location created successfully"})
        else:
            return render(request,"manager/new_location.html",{"form":form})
    else:
        form=locationForm()
        return render(request,"manager/new_location.html",{"form":form})


def showUsers(request):
    users=None
    if request.method == "POST":
        data=request.POST.dict()
        if 'search' in request.POST:
            response=render(request,"manager/showusers.html",{"users":manager.function.getUsers(data),"u":data['username'],"f":data['fullname'],"e":data['email'],"r":data['role']})
            response.set_cookie("u",data['username'])
            response.set_cookie("f",data['fullname'])
            response.set_cookie("e",data['email'])
            response.set_cookie("r",data['role'])
            return response
        else:
            manager.function.deleteUser(list(data)[1])
            data={'username':request.COOKIES['u'],'fullname':request.COOKIES['f'],'email':request.COOKIES['e'],'role':request.COOKIES['r']}
            return render(request,"manager/showusers.html",{"users":manager.function.getUsers(data),"u":data['username'],"f":data['fullname'],"e":data['email'],"r":data['role']})    
    else:
        return render(request,"manager/showusers.html",{"users":users})






def createuser(request,msg=''):
    if request.method == "POST" :
        form=userForm(request.POST) 
        if form.is_valid():
            form.save()
            msg='User created successfully'
            return render(request,"manager/createuser.html",{"form":form,"message":msg})
        else:
            return render(request,"manager/createuser.html",{"form":form,"message":msg})
    else:
        form=userForm()
        return render(request,"manager/createuser.html",{"form":form,"message":msg})


def showInventory(request):
    if request.method == "POST":
        data=request.POST.dict()       
        #define place for message 
        #fix search again by same filters
        #filter still need fixing 
        if 'search' in request.POST:
            response= render(request,"manager/showInventory.html",{"inventorys":manager.function.getInventory(data),"s":data['sku'],"n":data['name'],"l":data['location']})
            response.set_cookie('s',data['sku'])
            response.set_cookie('l',data['location'])
            response.set_cookie('n',data['name'])
            response.set_cookie('c',data['category'])
            return response
        else:
            key=list(data)[0]
            message=manager.function.updateAmount(key,data[key])
            data={'sku':request.COOKIES['s'],'location':request.COOKIES['l'],'name':request.COOKIES['n'],'category':request.COOKIES['c']}
            return render(request,"manager/showInventory.html",{"inventorys":manager.function.getInventory(data),"s":data['sku'],"n":data['name'],"l":data['location'], 'message':message})   
    else:
        return render(request,"manager/showInventory.html",{'inventorys':None})
