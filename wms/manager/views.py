from django.shortcuts import render,HttpResponse,redirect
import manager.function
from manager.forms import productForm,locationForm,userForm
from website.models import user,inventory,products,categories
from datetime import datetime
import xlwt
from django.db.models import Sum

def menu(request):
    return render(request,"manager/menu.html",status=200)

def newLocation(request):
    """unit test at website/models.py """
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

def showUsers(request):
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



def createuser(request,msg=''):
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


def showInventory(request):
    if request.method == "POST":
        data=request.POST.dict()       
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

def reports(request):
    return render(request,'manager/reports.html')
    
def inventoryToExel(request):
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
    


