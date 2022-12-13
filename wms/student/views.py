from django.shortcuts import render
from student import function

def menu(request):
    return render(request,"student/menu.html")
    
def showInventory(request):
    if request.method == "POST":
        if 'search' in request.POST:
            return render(request,"student/showinventory.html",{"inventorys":function.sumInventory(request.POST.dict())})
        else:
            return render(request,"student/showinventory.html")    
    else:
        return render(request,"student/showinventory.html")

def showOrders(request):
    if request.method == "POST":
        if 'search' in request.POST:
            return render(request,"student/showorders.html",{"orders":function.sumOrders(request.POST.dict())})
        else:
            return render(request,"student/showorders.html")    
    else:
        return render(request,"student/showorders.html")

