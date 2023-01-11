from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from student import function
from website.models import orders,specific_order
from django.contrib.auth.decorators import login_required
from django.http import Http404
from datetime import datetime
from django.contrib import messages
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.db.models import Sum ,Avg
from student.forms import productChoose
def is_student(user):
    return str(user.role)=='Student'

@login_required
def menu(request):
    if not is_student(request.user):
        raise Http404
    return render(request,"student/menu.html",status=200)
  
@login_required
def watchOrder(request,order_id):
    if not is_student(request.user):
        raise Http404
    order=get_object_or_404(orders,order_number=order_id)
    form=productChoose()
    if request.method=='POST':
        if 'newItem' in request.POST:
            messages.success(request,function.newOrder_spec(request.POST.dict(),order))
            return redirect('watchorder',order_id=order_id)
        else:
            function.deleteItem(int(list(request.POST.dict())[1]),order)
            return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order),'form':form},status=200)
    else:
        return render(request,'student/watchOrder.html',{'order':order,'o_list':function.getOrderlist(order),'form':form},status=200)

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
def products_To_Excel_for_student(request):
    if not is_student(request.user):
        raise Http404 

    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Products'+str(datetime.now())+'.xls'
    function.create_list_products_excel_for_student().save(response)
    return response  



@login_required
def recepit(request,order_id): 
    order=get_object_or_404(orders,order_number=order_id)
    if not is_student(request.user) or order.user_id != request.user or order.status!=2:
        raise Http404
    def render_to_pdf(template_src, context_dict={}):
        template = get_template(template_src)
        html  = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    context =  {}
    context['order']=order
    context['o_list']=specific_order.objects.filter(order_id=context['order']).values('sku','sku__name','sku__price','inventory_id__serial','amount').annotate(sum_amount=Sum('amount'),total_price=Sum('amount')*Avg('sku__price'))
    context['total']=context['o_list'].aggregate(Sum('sum_amount'),Sum("total_price"))
    print(context['total'])
    pdf = render_to_pdf('student/recepit.html', context) 
     
    response = HttpResponse(pdf, content_type='application/pdf')  
    response['Content-Disposition']='inline; attachment; filename=Recepit'+str(order_id)+'.pdf'
    return response 
    

@login_required    
def price_To_Excel(request):
    if not is_student(request.user):
        raise Http404 

    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Price list.xls'
    function.create_price_list_excel().save(response)
    return response  