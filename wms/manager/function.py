from website.models import user1,inventory


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
    try:
        delete=user1.objects.get(username=userTodelete)
    except:
        return
    delete.is_active=False
    delete.password=0
    delete.save()

def getInventory(data):
        kwargs={}
        if data['sku'] != '':
            kwargs['sku__sku']=data['sku']
        if data['location'] != '':
            kwargs['location__location']=data['location']
        if data['category'] != '':
             kwargs['sku__category']=data['category']
        return inventory.objects.filter(**kwargs).order_by('sku','location','-amount').select_related('sku','location')
        
 
def updateAmount(idInv,newAmount):
    """ unit tests in manager/tests.py """
    try:
        newAmount=int(newAmount)
        inven=inventory.objects.get(id=idInv)
        if (inven.amount-inven.available)<=newAmount:
            inven.available=inven.available+(newAmount-inven.amount)
            inven.amount=newAmount
            if inven.amount==0:
                inven.delete()
            else:
                inven.save()
            return (f"#{inven.sku.name} in {inven.location} updated to {newAmount}",'blue')
        else:
            return ("#The new amount does not match the quantity ordered",'red')
    except:
        return ('#EROR pls try again','red')
