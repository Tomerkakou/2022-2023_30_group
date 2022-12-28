from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from student import function
from website.models import orders
from django.contrib.auth.decorators import login_required
from django.http import Http404
from datetime import datetime
from django.contrib import messages

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
            messages.success(request,function.newOrder_spec(request.POST.dict(),order))
            return redirect('watchorder',order_id=order_id)
        else:
            function.deleteItem(int(list(request.POST.dict())[1]),order)
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
            return render(request,"student/showorders.html",{"orders":function.getOrders(request.POST.dict(),u)},status=200)
        else:
            function.deleteOrder(list(request.POST.dict())[1])
            return render(request,"student/showorders.html",status=200)    
    else:
        return render(request,"student/showorders.html",status=200)


@login_required
def reports(request):
    if not is_student(request.user):
        raise Http404
    return render(request,'student/reports.html')



@login_required    
def products_To_Excel_for_student(request):
    if not is_student(request.user):
        raise Http404 

    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Products'+str(datetime.now())+'.xls'
    function.create_list_products_excel_for_student().save(response)
    return response  



