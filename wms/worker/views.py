
from django.shortcuts import render

from website.models import inventory,products,newInventory,user
from worker import function
from worker.forms import inventoryForm
from manager.forms import productForm
def menu(request):
    return render(request,"worker/menu.html")



def inventory_receipt(request):
    if request.method == "POST" :
        form=inventoryForm(request.POST) 
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
        form=inventoryForm()
        return render(request,"worker/new_inventory.html",{"form":form})


def showInventory(request): 
    if request.method == "POST": 
        if 'search' in request.POST:   
            search = request.POST.dict()
            response=render(request,"worker/showinventory.html",{"l_inventory":function.getInventory(search),'s':search['sku'],'l':search['location'],'se':search['serial']})  
            response.set_cookie('s',search['sku'])
            response.set_cookie('l',search['location'])
            response.set_cookie('se',search['serial'])
            response.set_cookie('c',search['category'])
            return response
        else:
            pass#when change location is added 
    else:
        return render(request,"worker/showinventory.html",{"l_inventory":inventory.objects.all()})

def showProduct(request,id):
    p=products.objects.get(sku=id)
    form=productForm(initial={'sku':p.sku,'name':p.name,'descprition':p.descprition,'price':p.price,'category':p.category,'serial_item':p.serial_item})
    return render(request,"worker/product.html",{"product":form,'title':str(p)})

def productSearch(request):
    if request.method == 'POST':
        data=request.POST.dict()
        return render(request,"worker/productsearch.html",{'products':function.getProducts(data)})
    else:
        return render(request,"worker/productsearch.html")
