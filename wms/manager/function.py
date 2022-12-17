from website.models import products,locations,user1,inventory
from django.shortcuts import get_object_or_404

def getUsers(data):
    kwargs={'is_active':True}
    if data['username'] != '':
        kwargs['username']=data['username']
    if data['fullname'] != '':
        kwargs['full_name']=data['fullname']
    if data['email'] != '':
        kwargs['email']=data['email'] 
    if data['role'] != '':
        kwargs['role__id']=data['role']
    return user1.objects.filter(**kwargs)
 

def deleteUser(userTodelete):
    delete=user1.objects.get(username=userTodelete)
    delete.is_active=False
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
    """ unit tests in manager/tests.py """

    newAmount=int(newAmount)
    inven=get_object_or_404(inventory,id=idInv)
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

