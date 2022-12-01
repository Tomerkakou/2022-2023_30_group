from django.shortcuts import render
from website.models import inventory

def menu(request):
    return render(request,"student/menu.html")
    
def showInventory(request):
    if request.method == "POST":
        if 'search' in request.POST:
            """
            filter1=''
            filter2=''
            search=request.POST.dict()
            if search['sku']!='':
                filter1=f"AND username='{search['username']}'"
            if search['category']!='':
                filter2=f"AND name='{search['fullname']}'"
                """
            inv=inventory.objects.raw(f"SELECT DISTINCT sku_id ,SUM(available) as amount, id FROM website_inventory GROUP BY sku_id;")#f"SELECT * FROM `website_inventory` WHERE status=1 {filter1} {filter2} {filter3} {filter4};")   
            
            return render(request,"student/showinventory.html",{"inventorys":inv})
        else:
            return render(request,"student/showinventory.html")    
    else:
        return render(request,"student/showinventory.html")