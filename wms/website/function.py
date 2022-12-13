from website.models import user


def register(data):
    try:
        if data['reg_username']!= '' and data['reg_pass']!= '' and data['reg_name']!= '' and data['reg_email']!= '':
            user.objects.create(username=data['reg_username'],password=data['reg_pass'],name=data['reg_name'],email=data['reg_email'])
            return 'User created succsesfully'
        else:
            return "Not all details have been filled in"      
    except:
         return "Username or Email already in use"

def login(data):
    try:
            current= user.objects.get(username=data['username'])
            if current.password != data['password']:
                raise ValueError
            return  current 
    except:
            return None