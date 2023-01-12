from website.models import user1
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import password_validators_help_texts,validate_password
from django.forms import ValidationError
from functools import reduce

def register(data):
    if data['reg_username']!= '' and data['reg_pass']!= '' and data['reg_name']!= '' and data['reg_email']!= '':
        student=Group.objects.get(name='Student')
        if user1.objects.filter(username=data['reg_username']).count()==0:
            if user1.objects.filter(email=data['reg_email']).count()==0:
                try:
                    validate_password(data['reg_pass'])
                except ValidationError:
                    warning=password_validators_help_texts()
                    warning=reduce(lambda x,y:x+'\\n• '+y,warning,'')
                    return warning[2:]
                user=user1.objects.create_user(username=data['reg_username'],password=data['reg_pass'],full_name=data['reg_name'],email=data['reg_email'],role=student)
                return 'User created succsesfully'
            else:
                 return 'Email already in use'
        else:
            return 'Username already in use'
    else:
        return "Not all details have been filled in"      

def login(data):
    try:
            current= user1.objects.get(username=data['username'])
            if current.check_password(data['password']):
                return  current
            return 'Invalid username or password'      
    except:
            return 'Invalid username or password'