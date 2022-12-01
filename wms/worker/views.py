
from django.shortcuts import render, HttpResponse, redirect
from django.forms import modelform_factory
from website.models import inventory,products,newInventory,user
from website.views import curr

def menu(request):
    return render(request,"worker/menu.html")

inventory_form=modelform_factory(inventory,exclude=['available'])

def new_inventory(request):
    msg=''
    if request.method == "POST" :
        form=inventory_form(request.POST) 
        if form.is_valid():
            result=addNewInv(request.POST.dict())
            if result==0:
                form.save()
                inv=inventory.objects.get(available=-1)
                inv.available=inv.amount
                inv.save()
                form.clean()
                msg="Inventory created succsessfully"
                return render(request,"worker/new_inventory.html",{"form":form,'message':msg})
            elif result==1:
                msg="Item with serial number"
                return render(request,"worker/new_inventory.html",{"form":form,'message':msg})
            elif result==2:
                msg="Inventory created succsessfully"
                return render(request,"worker/new_inventory.html",{"form":form,'message':msg})
        else:
            return render(request,"worker/new_inventory.html",{"form":form})
    else:
        form=inventory_form()
        return render(request,"worker/new_inventory.html",{"form":form})
    
def addNewInv(form):
    product=products.objects.get(sku=int(form['sku']))
    if product.serial_item == 1 :
        if form['serial']!='' and int(form['amount'])==1:
            return 0
        else:
            return 1
    inv=inventory.objects.filter(sku=form['sku']).filter(location=form['location'])
    if len(inv)!=0:
        inv=inv.first()
        inv.amount+=int(form['amount'])
        inv.available+=int(form['amount'])
        inv.save()
        return 2
    
    return 0


