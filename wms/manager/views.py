from django.shortcuts import render,HttpResponse
import manager.function
from manager.forms import productForm,locationForm,userForm
from website.models import inventory,categories,newInventory, specific_order
from datetime import datetime,timedelta
import xlwt
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import Http404

def is_manager(user):
    return str(user.role)=='Manager'

@login_required
def menu(request):
    if not is_manager(request.user):
        raise Http404
    return render(request,'manager/menu.html')

@login_required
def newProduct(request):
    if not is_manager(request.user):
        raise Http404
    if request.method == "POST" :
        form=productForm(request.POST) 
        if form.is_valid():
            form.save()
            form=productForm()
            return render(request,"manager/new_product.html",{"form":form,"message":"New product created successfully"},status=201)
        else:
            return render(request,"manager/new_product.html",{"form":form},status=400)
    else:
        form=productForm()
        return render(request,"manager/new_product.html",{"form":form},status=200)

@login_required
def newLocation(request):
    """unit test at website/models.py """
    if not is_manager(request.user):
        raise Http404
    if request.method == "POST" :
        form=locationForm(request.POST) 
        if form.is_valid():
            form.save()
            form=locationForm()
            return render(request,"manager/new_location.html",{"form":form,"message":"Location created successfully"},status=201)
        else:
            return render(request,"manager/new_location.html",{"form":form},status=400)
    else:
        form=locationForm()
        return render(request,"manager/new_location.html",{"form":form},status=200)

@login_required
def showUsers(request):
    if not is_manager(request.user):
        raise Http404
    users=None
    if request.method == "POST":
        data=request.POST.dict()
        if 'search' in request.POST:
            response=render(request,"manager/showusers.html",{"users":manager.function.getUsers(data),"u":data['username'],"f":data['fullname'],"e":data['email'],"r":data['role']},status=200)
            response.set_cookie("u",data['username'])
            response.set_cookie("f",data['fullname'])
            response.set_cookie("e",data['email'])
            response.set_cookie("r",data['role'])
            return response
        else:
            manager.function.deleteUser(list(data)[1])
            data={'username':request.COOKIES['u'],'fullname':request.COOKIES['f'],'email':request.COOKIES['e'],'role':request.COOKIES['r']}
            return render(request,"manager/showusers.html",{"users":manager.function.getUsers(data),"u":data['username'],"f":data['fullname'],"e":data['email'],"r":data['role']},status=200)    
    else:
        return render(request,"manager/showusers.html",{"users":users},status=200)


def newProduct(request):
    """unit test at website/models.py """
    if request.method == "POST" :
        form=productForm(request.POST) 
        if form.is_valid():
            form.save()
            form=productForm()
            return render(request,"manager/new_product.html",{"form":form,"message":"New product created successfully"},status=201)
        else:
            return render(request,"manager/new_product.html",{"form":form},status=400)
    else:
        form=productForm()
        return render(request,"manager/new_product.html",{"form":form},status=200)


@login_required
def createuser(request,msg=''):
    if not is_manager(request.user):
        raise Http404
    if request.method == "POST" :
        form=userForm(request.POST) 
        if form.is_valid():
            form.save()
            form=userForm()
            msg='User created successfully'
            return render(request,"manager/createuser.html",{"form":form,"message":msg})
        else:
            return render(request,"manager/createuser.html",{"form":form,"message":msg})
    else:
        form=userForm()
        return render(request,"manager/createuser.html",{"form":form,"message":msg})

@login_required
def showInventory(request):
    if not is_manager(request.user):
        raise Http404
    if request.method == "POST":
        data=request.POST.dict()       
        if 'search' in request.POST:
            response= render(request,"manager/showInventory.html",{"inventorys":manager.function.getInventory(data),"s":data['sku'],"l":data['location']})
            response.set_cookie('s',data['sku'])
            response.set_cookie('l',data['location'])
            response.set_cookie('c',data['category'])
            return response 
        else:
            key=list(data)[0]
            message,color=manager.function.updateAmount(key,data[key])
            data={'sku':request.COOKIES['s'],'location':request.COOKIES['l'],'category':request.COOKIES['c']}
            return render(request,"manager/showInventory.html",{"inventorys":manager.function.getInventory(data),"s":data['sku'],"l":data['location'], 'message':message,'color':color}) 
    else:
        return render(request,"manager/showInventory.html",{'inventorys':None})

@login_required
def reports(request):
    if not is_manager(request.user):
        raise Http404
    return render(request,'manager/reports.html')

@login_required    
def inventoryToExel(request):
    if not is_manager(request.user):
        raise Http404
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Inventory'+str(datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Full inventory')
    row_num=0
    style = xlwt.easyxf('font: bold on, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    columns=['Sku','item name','Total amount','Total available','Category']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],style)

    

    sum_inventory=inventory.objects.raw(f"""SELECT inventory.id ,inventory.sku_id, inventory.sum_available,inventory.sum_amount, website_products.category ,website_products.name
                                        FROM  (SELECT id, sku_id ,SUM(available) as sum_available ,SUM(amount) as sum_amount
		                                FROM website_inventory
		                                GROUP BY sku_id) AS inventory
                                        RIGHT JOIN website_products 
                                        ON inventory.sku_id = website_products.sku;""")
    
    style = xlwt.easyxf('font: bold off, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    for row in sum_inventory:
        if row.sku_id is None:
            continue
        row_num+=1
        ws.write(row_num,0,row.sku_id,style)
        ws.write(row_num,1,row.name,style)
        ws.write(row_num,2,row.sum_amount,style)
        ws.write(row_num,3,row.sum_available,style)
        ws.write(row_num,4,categories[row.category][1],style)

    wb.save(response)

    return response
    




@login_required    
def report_entry_products(request):
    if not is_manager(request.user):
        raise Http404
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Entry products '+str(datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Entry products')
    row_num=0
    style = xlwt.easyxf('font: bold on, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    columns=['SKU','Item name','Entry amount']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],style)

    
    style = xlwt.easyxf('font: bold off, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    end , start = datetime.now(),datetime.now()+timedelta(weeks=-4)
    entrys=newInventory.objects.filter(dt__gte=start,dt__lte=end).values('sku','sku__name','amount').annotate(sum_amount=Sum('amount'))
    print(start,"\n",end)
    for row in entrys:
        row_num+=1
        ws.write(row_num,0,row['sku'],style)
        ws.write(row_num,1,row['sku__name'],style)
        ws.write(row_num,2,row['sum_amount'],style)
        

    wb.save(response)

    return response
    

@login_required    
def lendings_to_excel_for_manger(request):
    if not is_manager(request.user):
        raise Http404 

    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Stock on loan '+str(datetime.now())+'.xls'

    wb=xlwt.Workbook(encoding='utf-8')
    
    ws=wb.add_sheet('Stock on loan') 
    row_num=0
    style = xlwt.easyxf('font: bold on, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    columns=['SKU','Item name','Serial number','Loaned by','Return date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],style)

    
    result=specific_order.objects.filter(inventory_id__location__location='RETRNS').order_by('-id').values('sku__sku','sku__name','inventory_id__serial','order_id__user_id__full_name','order_id__return_date')[:len(inventory.objects.filter(location__location='RETRNS'))]
    style = xlwt.easyxf('font: bold off, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')

    for row in result:
        print(row)
        row_num+=1
        ws.write(row_num,0,row['sku__sku'],style)
        ws.write(row_num,1,row['sku__name'],style)
        ws.write(row_num,2,row['inventory_id__serial'],style)
        ws.write(row_num,3,row['order_id__user_id__full_name'],style)
        if row['order_id__return_date'] is None:
            ws.write(row_num,4,"Order not completed yet",style)
        else:
            ws.write(row_num,4,row['order_id__return_date'].strftime("%d/%m/%Y"),style)
        
                
                
                

    wb.save(response) 
    return response

