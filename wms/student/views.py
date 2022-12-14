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

        

def watchOrder(request,order_id):
    order=orders.objects.get(order_number=order_id)
    if request.method=='POST':
        if 'newItem' in request.POST:
            return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order),'message':function.newOrder_spec(request.POST.dict(),order)})
        else:
            function.deleteItem(list(request.POST.dict())[1])
            return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order)})
    else:
        return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order)})


def showOrders(request):
    if request.method == "POST":
        if 'neworder' in request.POST:
            u=user.objects.get(username=request.COOKIES['user'])
            order=orders.objects.create(user_id=u)
            return redirect('watchorder',order.order_number)
        if 'search' in request.POST:
            return render(request,"student/showorders.html",{"orders":function.sumOrders(request.POST.dict())})
        else:
            function.deleteOrder(list(request.POST.dict())[1])
            return render(request,"student/showorders.html")    
    else:
        return render(request,"student/showorders.html")

