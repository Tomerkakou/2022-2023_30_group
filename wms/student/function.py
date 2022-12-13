from website.models import inventory,orders
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


def sumOrders(data):
    print(data['create_date'])
    kwargs={}
    if data['order_number'] != '':
        kwargs['order_number']=data['order_number']
    if data['user_id'] != '':
        kwargs['user_id__username']=data['user_id']
    if data['create_date'] != '':
        date=data['create_date'].split('-')
        kwargs['create_date__gte']=datetime(int(date[0]),int(date[1]),int(date[2]))
    if data['return_date'] != '':
        date=data['return_date'].split('-')
        kwargs['return_date__lte']=datetime(int(date[0]),int(date[1]),int(date[2]))+timedelta(days=1)
    if data['status'] != '':
        kwargs['status']=data['status']

    return orders.objects.filter(**kwargs).order_by('status','create_date')