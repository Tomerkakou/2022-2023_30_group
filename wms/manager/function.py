from website.models import products,locations,user,inventory

def getUsers(data):
            filter1=''
            filter2=''
            filter3=''
            filter4=''
            if data['username']!='':
                filter1=f"AND username='{data['username']}'"
            if data['fullname']!='':
                filter2=f"AND name='{data['fullname']}'"
            if data['email']!='':
                filter3=f"AND email='{data['email']}'"
            if data['role']!='':
                filter4=f"AND role='{data['role']}'"
            return user.objects.raw(f"SELECT * FROM `website_user` WHERE status=1 {filter1} {filter2} {filter3} {filter4};") 

def deleteUser(userTodelete):
    delete=user.objects.get(username=userTodelete)
    delete.status=0
    delete.save()

def getInventory(data):
            filter1=''
            filter2=''
            filter3=''
            filter4=''
            if data['sku']!='':
                filter1==f" AND sku='{data['sku']}'"
            if data['name']!='':
                filter2=f" AND name='{data['name']}'"
            if data['location']!='':
                filter3=f" AND location='{data['location']}'"
            if data['category']!='':
                filter4=f" AND category='{data['category']}'"
            return inventory.objects.raw(f"""SELECT inventory.id ,inventory.sku_id, inventory.location_id, inventory.amount ,inventory.available ,inventory.serial, website_products.category ,website_products.name
                                        FROM  website_inventory AS inventory
                                        RIGHT JOIN website_products 
                                        ON inventory.sku_id = website_products.sku
                                        WHERE id>0{filter1}{filter2}{filter3}{filter4};""") 

def updateAmount(id,newAmount):
    inven=inventory.objects.get(id)
    if (inven.amount-inven.available)<=newAmount:
        inven.available=inven.available+(newAmount-inven.amount)
        inven.amount=newAmount
        inven.save()
        return f"{inven.sku.name} in {inven.location} updated to {newAmount}"
    else:
        return "The new amount does not match the quantity ordered" 
