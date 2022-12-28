
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from website.models import inventory,products,newInventory,orders,locations,categories
from worker import function
from worker.forms import inventoryForm,locationform
from manager.forms import productForm
from datetime import datetime
import xlwt 






def is_worker(user):
    return str(user.role)=='Worker'

@login_required
def menu(request):
    if not is_worker(request.user):
        raise Http404
    return render(request,"worker/menu.html",status=200)

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
        search = request.POST.dict()
        if 'search' in request.POST:   
            response=render(request,"worker/showinventory.html",{"l_inventory":function.getInventory(search),'s':search['sku'],'l':search['location_search'],'se':search['serial'],'form':locationform()},status=200)  
            response.set_cookie('s',search['sku'])
            response.set_cookie('l',search['location_search'])
            response.set_cookie('se',search['serial'])
            response.set_cookie('c',search['category'])
            return response
        else:
            print(search)
            inventory_id=int(tuple(search.keys())[2])
            new_location=search['location']
            msg=function.move_to(inventory_id,new_location)
            search['sku']=request.COOKIES['s']
            search['location_search']=request.COOKIES['l']
            search['serial']=request.COOKIES['se']
            search['category']=request.COOKIES['c']
            return render(request,"worker/showinventory.html",{"l_inventory":function.getInventory(search),'s':search['sku'],'l':search['location_search'],'se':search['serial'],'form':locationform(),'message':msg},status=200)
    else:
        return render(request,"worker/showinventory.html",status=200)

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

@login_required
def showOrders(request):
    if not is_worker(request.user):
        raise Http404
    if request.method == "POST":
        if 'search' in request.POST:
            return render(request,"worker/showorders.html",{"orders":function.getOrders(request.POST.dict())},status=200)   
    else:
        return render(request,"worker/showorders.html",status=200)

@login_required
def watchOrder(request,order_id):
    if not is_worker(request.user):
        raise Http404
    order=get_object_or_404(orders,order_number=order_id)
    if request.method=='POST':
        data=request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        data.pop('submit')
        order.status=function.completeOrder_list(tuple(map(lambda x: int(x),data.keys())),order)
        return render(request,'worker/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order)},status=200)
    else:
        return render(request,'worker/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order)},status=200)


@login_required
def showReturns(request): 
    if not is_worker(request.user):
        raise Http404
    if request.method == "POST": 
        if 'search' in request.POST:   
            search = request.POST.dict()
            response=render(request,"worker/returns.html",{"l_returns":function.get_returns(search),"form":locationform(),'s':search['sku'],'se':search['serial']},status=200)  
            response.set_cookie('s',search['sku'])
            response.set_cookie('se',search['serial'])
            response.set_cookie('c',search['category'])
            return response
        else:
            data=request.POST.dict()
            data['sku']=request.COOKIES['s']
            data['serial']=request.COOKIES['se']
            data['category']=request.COOKIES['c']
            inventory_id=int(tuple(data.keys())[2])
            new_location=data['location']
            try:
                obj=inventory.objects.get(id=inventory_id)
                obj.location=locations.objects.get(location=new_location)
                obj.setAvailable()
                msg=f'{obj.sku.name} with serial:{obj.serial} moved to {new_location}'
            except:
                msg=None
            return render(request,"worker/returns.html",{"l_returns":function.get_returns(data),"form":locationform(),'s':request.COOKIES['s'],'se':request.COOKIES['se'],'message':msg},status=200)
    else:
        return render(request,"worker/returns.html",status=200)





@login_required
def reports_for_worker(request):
    if not is_worker(request.user):
        raise Http404
    return render(request,'worker/reports.html')


@login_required    
def inventory_To_Excel_for_worker(request):
    if not is_worker(request.user):
        raise Http404 

    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Inventory'+str(datetime.now())+'.xls'
    function.create_excel_for_worker().save(response)
    return response  
    


