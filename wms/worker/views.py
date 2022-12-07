
from django.shortcuts import render, HttpResponse, redirect
from django.forms import modelform_factory
from website.models import inventory,products,newInventory,user
from worker import function
def menu(request):
    return render(request,"worker/menu.html")

inventory_form=modelform_factory(inventory,exclude=['available'])

def inventory_receipt(request):
    if request.method == "POST" :
        form=inventory_form(request.POST) 
        if form.is_valid():
            try:
                msg=function.addNewInv(request.POST.dict(),form,user.objects.get(username=request.COOKIES['user']))
            except:
                msg2="Item with serial number"
                return render(request,"worker/new_inventory.html",{"form":form,"message2":msg2})

            return render(request,"worker/new_inventory.html",{"form":form,"message":msg})
        else:
            return render(request,"worker/new_inventory.html",{"form":form})
    else:
        form=inventory_form()
        return render(request,"worker/new_inventory.html",{"form":form})


def showInventory(request): 
    if request.method == "POST": 
        if 'search' in request.POST:   
            seacrh = request.POST.dict()
            kwargs={}
            if seacrh['sku'] != '':
                kwargs['sku__sku']=seacrh['sku']
            if seacrh['location'] != '':
                kwargs['location__location']=seacrh['location']
            if seacrh['serial'] != '':
                kwargs['serial']=seacrh['serial'] 
            if seacrh['category'] != '':
                kwargs['sku__category']=seacrh['category']
            i_list=inventory.objects.filter(**kwargs).order_by('sku','location','-amount')
            return render(request,"worker/showinventory.html",{"l_inventory":i_list})  
    else:
        return render(request,"worker/showinventory.html",{"l_inventory":inventory.objects.all()})

def showProduct(request,id):
    product=products.objects.get(sku=id)
    return render(request,"worker/product.html",{"product":product})

