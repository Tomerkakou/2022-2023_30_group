from website.models import products,locations,user

def getUsers(data):
            filter1=''
            filter2=''
            filter3=''
            filter4=''
            if data['username']!='':
                filter1=f"AND username='{data['username']}'"
            if data['fullname']!='':
                filter2=f"AND name='{data['fullname']}'"
            if data['email']!='':
                filter3=f"AND email='{data['email']}'"
            if data['role']!='':
                filter4=f"AND role='{data['role']}'"
            return user.objects.raw(f"SELECT * FROM `website_user` WHERE status=1 {filter1} {filter2} {filter3} {filter4};") 

def deleteUser(userTodelete):
    delete=user.objects.get(username=userTodelete)
    delete.status=0
    delete.save()