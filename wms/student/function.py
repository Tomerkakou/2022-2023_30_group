
from website.models import inventory,specific_order,products,orders,categories
from django.db.models import Sum
from datetime import datetime, timedelta
import xlwt

def sumInventory(data):
    kwargs={'available__gt':0}
    if data['sku']!='':
        kwargs['sku__sku']={data['sku']}
    if data['category']!='':
        kwargs['sku__category']={data['category']}
    if data['name']!='':
        kwargs['sku__name__contains']={data['name']}

    return inventory.objects.filter(**kwargs).values('sku','sku__name','available','sku__category').annotate(sum_amount=Sum('available'))

    """filter1=''
    filter2=''
    filter3=''
    
    if data['sku']!='':
        filter1=f" AND sku_id='{data['sku']}'"
    if data['category']!='':
        filter2=f" AND category='{data['category']}'"
    if data['name']!='':
        filter3=f" AND name LIKE '%%{data['name']}%%'"
    
    inv=inventory.objects.raw(f#SELECT inventory.id ,inventory.sku_id, inventory.amount, website_products.category ,website_products.name
                                FROM  (SELECT id, sku_id ,SUM(available) as amount
                                FROM website_inventory
                                GROUP BY sku_id) AS inventory
                                RIGHT JOIN website_products 
                                ON inventory.sku_id = website_products.sku
                                WHERE amount>0{filter1}{filter2}{filter3};)
    return inv"""


def getOrders(data,user):
    print(data['create_date'])
    kwargs={'user_id':user}
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

    return orders.objects.filter(**kwargs).order_by('status','-create_date')

def getOrderlist(order):
    
    return specific_order.objects.filter(order_id=order).values('sku','sku__name','completed').annotate(sum_amount=Sum('amount')).order_by('sku','completed')
     

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
            check=specific_order.objects.filter(inventory_id=inv,completed=False,order_id=order_obj)
            if check.exists():
                check=check.first()
                check.amount+=curr_amount
                check.save()
            else:
                specific_order.objects.create(order_id=order_obj,sku=product,amount=curr_amount,inventory_id=inv)
            inv.available=inv.available-curr_amount
            amount_orderd=amount_orderd-curr_amount
            inv.save()
            index+=1
        return None
            
    
def deleteItem(sku_num,order=None):
    if isinstance(sku_num,specific_order):
        item=sku_num
        item.inventory_id.available+=item.amount
        item.inventory_id.save()
        item.delete()
    else:
        items=specific_order.objects.filter(order_id=order,sku__sku=sku_num)
        for item in items:
            item.inventory_id.available+=item.amount
            item.inventory_id.save()
            item.delete()

    

def deleteOrder(or_num):
    try:
        order=orders.objects.get(order_number=or_num)
    except:
        return
    o_list=specific_order.objects.filter(order_id=order)
    for i in o_list:
        deleteItem(i)
    order.delete()


def create_list_products_excel_for_student():
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Products list')
    row_num=0
    style = xlwt.easyxf('font: bold on, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    columns=['Category','Item name','SKU','Description','Price','Only for borrow','availble/Unavailble']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],style)

    

    sum_inventory=inventory.objects.raw(f"""SELECT inventory.id ,inventory.sku_id, inventory.sum_available, website_products.category ,website_products.name ,website_products.description ,website_products.price ,website_products.serial_item
                                        FROM  (SELECT id, sku_id ,SUM(available) as sum_available 
		                                FROM website_inventory
		                                GROUP BY sku_id) AS inventory
                                        RIGHT JOIN website_products 
                                        ON inventory.sku_id = website_products.sku;""")

    style = xlwt.easyxf('font: bold off, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    for row in sum_inventory:
        if row.sku_id is None:
            continue
        row_num+=1
        ws.write(row_num,0,categories[row.category][1],style)
        ws.write(row_num,1,row.name,style)
        ws.write(row_num,2,row.sku_id,style)
        ws.write(row_num,3,row.description,style)
        ws.write(row_num,4,row.price,style)
        if row.serial_item ==1:
            ws.write(row_num,5,'YES',style)
        else:
            ws.write(row_num,5,'NO',style)
        if row.sum_available>0:
             ws.write(row_num,6,'availble',style)
        else:
             ws.write(row_num,6,'Unavailble',style)

    return wb


def create_price_list_excel():
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Price list')
    row_num=0
    style = xlwt.easyxf('font: bold on, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    columns=['Item name','SKU','Price']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],style)

    

    product_list= products.objects.all()
    style = xlwt.easyxf('font: bold off, color black; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
    for row in product_list:
        row_num+=1
        ws.write(row_num,0,row.name,style)
        ws.write(row_num,1,row.sku,style)
        ws.write(row_num,2,row.price,style)
    return wb