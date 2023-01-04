from django.shortcuts import render ,redirect,HttpResponse
import website.function as function
from website.models import user1
from django.contrib.auth import update_session_auth_hash
from website.forms import user_updateForm,PasswordChangeCustomForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

@login_required
def log_out(request):
    logout(request)
    return redirect('login')
            
def start(request):
    if request.method=="POST":
        if "login" in request.POST :
            login_data = request.POST.dict()
            current=function.login(login_data)
            print(type(current))
            if current:
                login(request,current)
                return redirect(f"{current.role}_menu")
            else:
                return render(request,"website/login-register.html",{'message':"Invalid username or password"},status=401)
        elif "register" in request.POST :
            return render(request,"website/login-register.html",{'message2': function.register(request.POST.dict())})
    else:
        return render(request,"website/login-register.html",status=200)

@login_required
def changeUser(request):
    u=request.user
    if u.role_id == 1:
        x='manager/menu.html'   
    elif u.role_id == 2:
        x='worker/menu.html'  
    elif u.role_id == 3:
        x='student/menu.html'
    if request.method == 'POST':
        if 'change_info' in request.POST:
            form1=user_updateForm(request.POST,instance=u)
            form2=PasswordChangeCustomForm(user=u)
            if form1.is_valid():
                form1.save()
                msg='User information updated successfully'
                return render(request,f"website/userupdate.html",{"form1":form1,'form2':form2,"message":msg,'menu':x},status=200)
            else:
                return render(request,f"website/userupdate.html",{"form1":form1,'form2':form2,'menu':x},status=400)
        if 'change_password' in request.POST:
            form1=user_updateForm(instance=u)
            form2=PasswordChangeCustomForm(request.user,request.POST)
            if form2.is_valid():
                user=form2.save()
                update_session_auth_hash(request, user)
                msg='User password updated successfully'
                return render(request,f"website/userupdate.html",{"form1":form1,'form2':form2,"message2":msg,'menu':x},status=200)
            else:
                return render(request,f"website/userupdate.html",{"form1":form1,'form2':form2,'menu':x},status=400)
    else:
        form1=user_updateForm(instance=u)#initial={'username':u.username,'password':u.password,'email':u.email,'name':u.name})
        form2=PasswordChangeCustomForm(user=u)
        return render(request,f"website/userupdate.html",{"form1":form1,'form2':form2,'menu':x},status=200) 