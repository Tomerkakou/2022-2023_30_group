
from website.models import inventory,specific_order,products,orders
from django.db.models import Sum
from datetime import datetime, timedelta

def sumInventory(data):
            filter1=''
            filter2=''
            filter3=''

            if data['sku']!='':
                filter1=f" AND sku_id='{data['sku']}'"
            if data['category']!='':
                filter2=f" AND category='{data['category']}'"
            if data['name']!='':
                filter3=f" AND name LIKE '%%{data['name']}%%'"
            
            inv=inventory.objects.raw(f"""SELECT inventory.id ,inventory.sku_id, inventory.amount, website_products.category ,website_products.name
                                        FROM  (SELECT id, sku_id ,SUM(available) as amount
		                                FROM website_inventory
		                                GROUP BY sku_id) AS inventory
                                        RIGHT JOIN website_products 
                                        ON inventory.sku_id = website_products.sku
                                        WHERE amount>0{filter1}{filter2}{filter3};""")
            return inv


def sumOrders(data,user):
    print(data['create_date'])
    kwargs={'user_id':user}
    if data['order_number'] != '':
        kwargs['order_number']=data['order_number']
    if data['create_date'] != '':
        date=data['create_date'].split('-')
        kwargs['create_date__gte']=datetime(int(date[0]),int(date[1]),int(date[2]))
    if data['return_date'] != '':
        date=data['return_date'].split('-')
        kwargs['return_date__lte']=datetime(int(date[0]),int(date[1]),int(date[2]))+timedelta(days=1)
    if data['status'] != '':
        kwargs['status']=data['status']

    return orders.objects.filter(**kwargs).order_by('status','create_date')

def getOrderlist(order):
    
    return specific_order.objects.filter(order_id=order)

def newOrder_spec(data,order_obj):
    try:
        amount_orderd=int(data['amount'])
        product=products.objects.get(sku=data['sku'])
    except:
        return 'Invalid sku'
    res=inventory.objects.filter(sku=product).aggregate(Sum('available'))
    if res['available__sum']<amount_orderd or amount_orderd<1:
        return 'Invalid amount'
    else:
        
        inv_list=list(inventory.objects.filter(sku=product,available__gt=0).order_by('available'))
        index=0
        while amount_orderd >0:
            inv=inv_list[index]
            if amount_orderd<=inv.available:
                curr_amount=amount_orderd
            else:
                curr_amount=inv.available
            specific_order.objects.create(order_id=order_obj,sku=product,amount=curr_amount,inventory_id=inv)
            inv.available=inv.available-curr_amount
            amount_orderd=amount_orderd-curr_amount
            inv.save()
            index+=1
        return None
            
    
def deleteItem(id_num):
    if isinstance(id_num,specific_order):
        item=id_num
        
    else:
        item=specific_order.objects.get(id=id_num)
    item.inventory_id.available+=item.amount
    item.inventory_id.save()
    item.delete()

def deleteOrder(or_num):
    order=orders.objects.get(order_number=or_num)
    o_list=specific_order.objects.filter(order_id=order)
    for i in o_list:
        deleteItem(i)
    order.delete()
