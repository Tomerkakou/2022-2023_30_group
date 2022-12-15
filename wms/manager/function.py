from website.models import products,locations,user,inventory

def getUsers(data):
    kwargs={'status':1}
    if data['username'] != '':
        kwargs['username']=data['username']
    if data['fullname'] != '':
        kwargs['name']=data['fullname']
    if data['email'] != '':
        kwargs['email']=data['email'] 
    if data['role'] != '':
        kwargs['role']=data['role']
    return user.objects.filter(**kwargs)
 

def deleteUser(userTodelete):
    delete=user.objects.get(username=userTodelete)
    delete.status=0
    delete.save()

def getInventory(data):
        kwargs={}
        if data['sku'] != '':
            kwargs['sku__sku']=data['sku']
        if data['location'] != '':
            kwargs['location__location']=data['location']
        if data['name'] != '':
            kwargs['sku__name']=data['name'] 
        if data['category'] != '':
             kwargs['sku__category']=data['category']
        return inventory.objects.filter(**kwargs).order_by('sku','location','-amount').select_related('sku','location')
        
 
def updateAmount(idInv,newAmount):
    newAmount=int(newAmount)
    inven=inventory.objects.get(id=idInv)
    if (inven.amount-inven.available)<=newAmount:
        inven.available=inven.available+(newAmount-inven.amount)
        inven.amount=newAmount
        if inven.amount==0:
            inven.delete()
        else:
            inven.save()
        return f"#{inven.sku.name} in {inven.location} updated to {newAmount}"
    else:
        return "#The new amount does not match the quantity ordered"

