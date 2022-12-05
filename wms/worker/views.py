
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
    
def showInventory(request): 
    l_inventory = None
    if request.method == "POST": 
        #if 'search' in request.Post:   
        seacrh = request.POST.dict() #what is this func 
        l_inventory = inventory.objects.all()
        i_list = list()
        for i in l_inventory: 
            flag = 1 
            if seacrh['sku'] != '' and str(i.sku)!=seacrh['sku']:
                flag = 0 
            if seacrh['location'] != '' and str(i.location)!=seacrh['location']:
                flag = 0 
            if seacrh['amount'] != '' and str(i.amount)!=seacrh['amount']:
                flag = 0 
            if seacrh['available'] != '' and str(i.available)!=seacrh['available']:
                flag = 0 
            if seacrh['serial'] != '' and str(i.serial)!=seacrh['serial']:
                flag = 0 
            if flag == 1:
                i_list.append(i) #add inventory to the list  
        if i_list == None:
            msg='Missing product'
            return render(request,"worker/show inventory.html",{"form":i_list,"message":msg}) 
        else:
            return render(request,"manager/showInventory.html",{"l_inventory":i_list})  
    else:
        return render(request,"manager/showInventory.html",{"l_inventory":l_inventory})


                
