
from django.shortcuts import render, HttpResponse, redirect
from django.forms import modelform_factory
from website.models import inventory,products,newInventory
from website.views import curr

def menu(request):
    return render(request,"worker/menu.html")

inventory_form=modelform_factory(inventory,fields=("location","sku","amount","serial"))

def new_inventory(request):
    msg=''
    if request.method == "POST" :
        form=inventory_form(request.POST) 
        if form.is_valid():
            if addNewInv(request.POST.dict()):
                form.save()
                return redirect('menu')
            else:
                msg="Item with serial number"
                return render(request,"worker/new_inventory.html",{"form":form,'message':msg})
        else:
            return render(request,"worker/new_inventory.html",{"form":form})
    else:
        form=inventory_form()
        return render(request,"worker/new_inventory.html",{"form":form})
    
def addNewInv(form):
    product=products.objects.get(sku=form['sku'])
    if product.serial_item ==1 :
        if form['serial']!=0 and form['amout']==1:
            newInventory.objects.create(amount=form['amout'],sku=form['sku'],user=curr.username).save()
            return True
        else:
            return False

    inv=inventory.objects.filter(sku=form['sku']).filter(location=form['location'])
    
    if len(inv)!=0:
        inv.amount+=int(form['amout'])
        inv.available+=int(form['amout'])
        inv.save()
        return False
    return True
    
