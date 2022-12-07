from website.models import inventory
from django.db.models import Sum

def sumInventory(data):
            filter1=''
            filter2=''
            filter3=''

            if data['sku']!='':
                filter1=f" AND sku_id='{data['sku']}'"
            if data['category']!='':
                filter2=f" AND category='{data['category']}'"
            if data['name']!='':
                filter3=f" AND name LIKE '%%{data['name']}%%'"
            
            inv=inventory.objects.raw(f"""SELECT inventory.id ,inventory.sku_id, inventory.amount, website_products.category ,website_products.name
                                        FROM  (SELECT id, sku_id ,SUM(available) as amount
		                                FROM website_inventory
		                                GROUP BY sku_id) AS inventory
                                        RIGHT JOIN website_products 
                                        ON inventory.sku_id = website_products.sku
                                        WHERE amount>0{filter1}{filter2}{filter3};""")
            return inv
