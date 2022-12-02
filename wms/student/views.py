from django.shortcuts import render
from website.models import inventory

def menu(request):
    return render(request,"student/menu.html")
    
def showInventory(request):
    if request.method == "POST":
        if 'search' in request.POST:
            
            filter1=''
            filter2=''
            filter3=''

            search=request.POST.dict()

            if search['sku']!='':
                filter1=f" AND sku_id='{search['sku']}'"
            if search['category']!='':
                filter2=f" AND category='{search['category']}'"
            #if search['name']!='': # add back to query
                #filter3=f" AND name LIKE '%{search['name']}%'"

            inv=inventory.objects.raw(f"""SELECT inventory.id ,inventory.sku_id, inventory.amount, website_products.category ,website_products.name
                                        FROM  (SELECT id, sku_id ,SUM(available) as amount
		                                FROM website_inventory
		                                GROUP BY sku_id) AS inventory
                                        RIGHT JOIN website_products 
                                        ON inventory.sku_id = website_products.sku
                                        WHERE amount>0{filter1}{filter2};""")
            
            return render(request,"student/showinventory.html",{"inventorys":inv})
        else:
            return render(request,"student/showinventory.html")    
    else:
        return render(request,"student/showinventory.html")