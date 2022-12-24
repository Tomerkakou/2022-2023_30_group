from website.models import inventory,products,newInventory,orders,specific_order
from datetime import datetime,timedelta
from django.db.models import Count

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
    if data['location'] != '':
        kwargs['location__location']=data['location']
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
    
            