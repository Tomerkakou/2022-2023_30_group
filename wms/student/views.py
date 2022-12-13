from django.shortcuts import render,redirect
from student import function
from website.models import user,orders

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

def newOrder(request):
        u=user.objects.get(username=request.COOKIES['user'])
        order=orders.objects.create(user_id=u)
        return redirect('watchorder',order.order_number)

def watchOrder(request,order_id):
    if request.method=='POST':
        pass#inventory choose
    else:
        order=orders.objects.get(order_number=order_id)
        return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order)})
