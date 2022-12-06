from website.models import products,locations,user

def getUsers(data):
    kwargs={}
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