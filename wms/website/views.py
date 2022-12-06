from django.shortcuts import render ,redirect
import website.function as function


            
def start(request):
    if request.method=="POST":
        if "login" in request.POST :
            login_data = request.POST.dict()
            current=function.login(login_data)
            if current:
                response=redirect(f"{current.get_role()}/menu/")
                response.set_cookie('user',current.username)
                return response
            else:
                return render(request,"website/login.html",{'message':"Invalid username or password"})
        elif "register" in request.POST :
            return render(request,"website/login.html",{'message2': function.register(request.POST.dict())})
    else:
        return render(request,"website/login.html")


