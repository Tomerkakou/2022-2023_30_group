from website.models import inventory,products,newInventory,orders,specific_order,locations,categories
from django.shortcuts import HttpResponse
from datetime import datetime,timedelta
from django.db.models import Count
import xlwt


def addNewInv(data,form,user):
    product=products.objects.get(sku=int(data['sku']))
    if product.serial_item == 1 :
        if data['serial']=='' or int(data['amount'])>1:
            raise ValueError
        else:
            temp=form.save()
            temp.setAvailable()
    else:
        inv=inventory.objects.filter(sku=data['sku']).filter(location=data['location'])
        #checks if there is the same product in the same location
        if len(inv)!=0:
            inv=inv.first()
            inv.amount+=int(data['amount'])
            inv.available+=int(data['amount'])
            inv.save()
        else:
            form.save()
            temp=inventory.objects.get(available=-1)
            temp.setAvailable()
    
    
    newInventory.objects.create(sku=product,user_id=user,amount=data['amount'])      
    return 'The inventory has been successfully received'

def getInventory(data):
    
    kwargs={}
    if data['sku'] != '':
        kwargs['sku__sku']=data['sku']
    if data['location_search'] != '':
        kwargs['location__location']=data['location_search']
    if data['serial'] != '':
        kwargs['serial']=data['serial'] 
    if data['category'] != '':
        kwargs['sku__category']=data['category']

    return inventory.objects.filter(**kwargs).exclude(location__location='RETRNS').order_by('sku','location','-amount')

def getProducts(data):
    kwargs={}
    if data['sku'] != '':
        kwargs['sku']=data['sku']
    if data['name'] != '':
        kwargs['name__contains']=data['name']
    if data['category'] != '':
        kwargs['category']=data['category']

    return products.objects.filter(**kwargs).order_by('sku','category')

def getOrders(data):
    print(data['create_date'])
    kwargs={}
    if data['order_number'] != '':
        kwargs['order_number']=data['order_number']
    if data['create_date'] != '':
        date=data['create_date'].split('-')
        kwargs['create_date__gte']=datetime(int(date[0]),int(date[1]),int(date[2]))
    if data['create_date_end'] != '':
        date=data['create_date_end'].split('-')
        kwargs['create_date__lte']=datetime(int(date[0]),int(date[1]),int(date[2]))+timedelta(days=1)
    if data['status'] != '':
        kwargs['status']=data['status']

    return orders.objects.filter(**kwargs).order_by('status','create_date')

def getOrderlist(order):
    
    return specific_order.objects.filter(order_id=order)

def completeOrder_list(id_list,order):
    order_list=getOrderlist(order)
    count=0
    for i in order_list:
        if i.id in id_list:
            count+=1
            i.complete()
    if count:
        order.status=1
    total=tuple(order_list.aggregate(Count('id')).values())[0]
    completed=tuple(order_list.filter(completed=True).aggregate(Count('id')).values())[0]
    if total==completed:
        order.complete_order()
    order.save()
    return order.status

def get_returns(data):
    kwargs={"location__location":"RETRNS"}
    if data['sku'] != '':
        kwargs['sku__sku']=data['sku']
    if data['serial'] != '':
        kwargs['serial']=data['serial'] 
    if data['category'] != '':
        kwargs['sku__category']=data['category']

    return inventory.objects.filter(**kwargs).order_by('sku','-amount')

def move_to(id,location):
    try:
        new_location=locations.objects.get(pk=location)
        inv=inventory.objects.get(pk=id)
        if inv.serial is None:
            exsisting_inv=inventory.objects.filter(sku=inv.sku,location=new_location)
            if exsisting_inv.exists():
                exsisting_inv=exsisting_inv.first()
                exsisting_inv.amount+=inv.amount
                exsisting_inv.available+=inv.available
                orderToChange=specific_order.objects.filter(inventory_id=inv,completed=False)
                for order in orderToChange:
                    order.inventory_id=exsisting_inv
                    order.save()
                inv.delete()
                exsisting_inv.save()
                return f'item: {inv.sku.name} moved to {new_location}'
        inv.location=new_location
        inv.save()
        return f'item: {inv.sku.name} moved to {new_location}'
    except:
        return None
        


def create_excel_for_worker():
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Full inventory')
    row_num=0
    style = xlwt.easyxf('font: bold on, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    columns=['Sku','Location','Serial number','item name','Amount','Available','Category']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],style)

    

    sum_inventory=inventory.objects.exclude(location__location='RETRNS')

    style = xlwt.easyxf('font: bold off, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    for row in sum_inventory:
        row_num+=1
        ws.write(row_num,0,row.sku.sku,style)
        ws.write(row_num,1,row.location.location,style)
        ws.write(row_num,2,row.serial,style)
        ws.write(row_num,3,row.sku.name,style)
        ws.write(row_num,4,row.amount,style)
        ws.write(row_num,5,row.available,style)
        ws.write(row_num,6,row.sku.return_category(),style)

    return wb 
    



