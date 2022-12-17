from website.models import user
from django.contrib.auth.models import User,Group


def register(data):
    try:
        if data['reg_username']!= '' and data['reg_pass']!= '' and data['reg_name']!= '' and data['reg_email']!= '':
            user1=User.objects.create_user(username=data['reg_username'],password=data['reg_pass'],first_name=data['reg_name'],email=data['reg_email'])
            student=Group.objects.get(name='Student')
            user1.groups.add(student)
            return 'User created succsesfully'
        else:
            return "Not all details have been filled in"      
    except:
         return "Username or Email already in use"

def login(data):
    try:
            current= User.objects.get(username=data['username'])
            if current.check_password(data['password']):
                return  current
            raise ValueError        
    except:
            return None