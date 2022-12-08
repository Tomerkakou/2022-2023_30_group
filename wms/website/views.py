from django.shortcuts import render ,redirect,HttpResponse
import website.function as function
from website.models import user
from website.forms import user_updateForm

            
def start(request):
    if request.method=="POST":
        if "login" in request.POST :
            login_data = request.POST.dict()
            current=function.login(login_data)
            if current:
                response=redirect(f"{current.get_role()}_menu")
                response.set_cookie('user',current.username)
                response.set_cookie('role',current.role)
                return response
            else:
                return render(request,"website/login-register.html",{'message':"Invalid username or password"})
        elif "register" in request.POST :
            return render(request,"website/login-register.html",{'message2': function.register(request.POST.dict())})
    else:
        return render(request,"website/login-register.html")


def changeUser(request):
    u=user.objects.get(username=request.COOKIES['user'])
    if u.role == 0:
        x='M'   
    elif u.role == 1:
        x='W'  
    elif u.role == 2:
        x='S'
    if request.method == 'POST':
        form=user_updateForm(request.POST,instance=u) 
        if form.is_valid():
            form.save()
            msg='User updated successfully'
            response=render(request,f"website/userupdate{x}.html",{"form":form,"message":msg})
            response.set_cookie('user',form.cleaned_data['username'])
            return response
        else:
            return render(request,f"website/userupdate{x}.html",{"form":form})
    else:
        form=user_updateForm(instance=u)#initial={'username':u.username,'password':u.password,'email':u.email,'name':u.name})
        return render(request,f"website/userupdate{x}.html",{"form":form}) 