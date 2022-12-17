
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from website.models import inventory,products,newInventory
from worker import function
from worker.forms import inventoryForm
from manager.forms import productForm

def is_worker(user):
    return str(user.role)=='Worker'

@login_required
def menu(request):
    if not is_worker(request.user):
        raise Http404
    return render(request,"worker/menu.html",{'user_name':request.COOKIES['user']},status=200)

def showInventory(request):
    """ unit test on worker/tests.py test_inventory_search"""
    if request.method == "POST": 
        if 'search' in request.POST:   
            search = request.POST.dict()
            response=render(request,"worker/showinventory.html",{"l_inventory":function.getInventory(search),'s':search['sku'],'l':search['location'],'se':search['serial']},status=200)  
            response.set_cookie('s',search['sku'])
            response.set_cookie('l',search['location'])
            response.set_cookie('se',search['serial'])
            response.set_cookie('c',search['category'])
            return response
        else:
            pass#when change location is added 
    else:
        return render(request,"worker/showinventory.html",{"l_inventory":inventory.objects.all()},status=200)

@login_required
def inventory_receipt(request):
    if not is_worker(request.user):
        raise Http404
    if request.method == "POST" :
        form=inventoryForm(request.POST) 
        if form.is_valid():
            try:
                msg=function.addNewInv(request.POST.dict(),form,request.user)
            except:
                msg2="Item with serial number"
                return render(request,"worker/new_inventory.html",{"form":form,"message2":msg2},status=400)
            form=inventoryForm()
            return render(request,"worker/new_inventory.html",{"form":form,"message":msg},status=201)
        else:
            return render(request,"worker/new_inventory.html",{"form":form},status=400)
    else:
        form=inventoryForm()
        return render(request,"worker/new_inventory.html",{"form":form},status=200)

@login_required
def showInventory(request): 
    if not is_worker(request.user):
        raise Http404
    if request.method == "POST": 
        if 'search' in request.POST:   
            search = request.POST.dict()
            response=render(request,"worker/showinventory.html",{"l_inventory":function.getInventory(search),'s':search['sku'],'l':search['location'],'se':search['serial']},status=200)  
            response.set_cookie('s',search['sku'])
            response.set_cookie('l',search['location'])
            response.set_cookie('se',search['serial'])
            response.set_cookie('c',search['category'])
            return response
        else:
            pass#when change location is added 
    else:
        return render(request,"worker/showinventory.html",{"l_inventory":inventory.objects.all()},status=200)

@login_required
def showProduct(request,id):
    if not is_worker(request.user):
        raise Http404
    p=get_object_or_404(products,sku=id)
    form=productForm(initial={'sku':p.sku,'name':p.name,'description':p.description,'price':p.price,'category':p.category,'serial_item':p.serial_item})
    form=productForm(initial={'sku':p.sku,'name':p.name,'description':p.description,'price':p.price,'category':p.category,'serial_item':p.serial_item})
    return render(request,"worker/product.html",{"product":form,'title':str(p)},status=200)

@login_required
def productSearch(request):
    if not is_worker(request.user):
        raise Http404
    if request.method == 'POST':
        data=request.POST.dict()
        return render(request,"worker/productsearch.html",{'products':function.getProducts(data)},status=200)
    else:
        return render(request,"worker/productsearch.html",status=200)
