from django.shortcuts import render,redirect,get_object_or_404
from student import function
from website.models import user1,orders
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404

def is_student(user):
    return str(user.role)=='Student'

@login_required
def menu(request):
    if not is_student(request.user):
        raise Http404
    return render(request,"student/menu.html",status=200)

@login_required    
def showInventory(request):
    if not is_student(request.user):
        raise Http404
    if request.method == "POST":
        if 'search' in request.POST:
            return render(request,"student/showinventory.html",{"inventorys":function.sumInventory(request.POST.dict())},status=200)
        else:
            return render(request,"student/showinventory.html",status=200)    
    else:
        return render(request,"student/showinventory.html",status=200)

        
@login_required
def watchOrder(request,order_id):
    if not is_student(request.user):
        raise Http404
    order=get_object_or_404(orders,order_number=order_id)
    if request.method=='POST':
        if 'newItem' in request.POST:
            return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order),'message':function.newOrder_spec(request.POST.dict(),order)},status=201)
        else:
            function.deleteItem(int(list(request.POST.dict())[1]))
            return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order)},status=200)
    else:
        return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order)},status=200)

@login_required
def showOrders(request):
    if not is_student(request.user):
        raise Http404
    if request.method == "POST":
        u=request.user
        if 'neworder' in request.POST:
            order=orders.objects.create(user_id=u)
            return redirect('watchorder',order.order_number)
        if 'search' in request.POST:
            return render(request,"student/showorders.html",{"orders":function.sumOrders(request.POST.dict(),u)},status=200)
        else:
            function.deleteOrder(list(request.POST.dict())[1])
            return render(request,"student/showorders.html",status=200)    
    else:
        return render(request,"student/showorders.html",status=200)

