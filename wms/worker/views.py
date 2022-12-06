
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
    


