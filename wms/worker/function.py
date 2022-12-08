from website.models import inventory,products,newInventory
def addNewInv(data,form,user):
    product=products.objects.get(sku=int(data['sku']))
    if product.serial_item == 1 :
        if data['serial']=='' or int(data['amount'])>1:
            raise ValueError
        else:
            form.save()
            temp=inventory.objects.get(available=-1)
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

    return inventory.objects.filter(**kwargs).order_by('sku','location','-amount')

def getProducts(data):
    kwargs={}
    if data['sku'] != '':
        kwargs['sku']=data['sku']
    if data['name'] != '':
        kwargs['name__contains']=data['name']
    if data['category'] != '':
        kwargs['category']=data['category']

    return products.objects.filter(**kwargs).order_by('sku','category')