from django.db import models
from enum import Enum
from datetime import datetime
from django.core.validators import EmailValidator , MinValueValidator

user_types = ( 
    (0, "manager"),
    (1, "worker"),
    (2, "student"))

categories=(# update in changes in show inventory
        (0,"Photographic products"),
        (1,"Writing Tools"),)

class user(models.Model):
    

    username=models.CharField(max_length=50,primary_key=True)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50,unique=True,validators=[EmailValidator(message='Invaild Email')])
    name=models.CharField(max_length=50)
    role=models.IntegerField(choices=user_types, default=2)
    status=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} is a {self.role}"

    def get_role(self):
        return user_types[self.role][1]


class products(models.Model):
    
    sku=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50 ,unique=True)
    price=models.FloatField()
    descprition=models.TextField()
    category=models.IntegerField(choices=categories)
    serial_item=models.IntegerField(choices=((0,'No'),(1,'Yes')))
    def __str__(self):
        return f"{self.sku}-{self.name}"
    def return_category(self):
        return categories[self.category][1]

class locations(models.Model):
    location=models.CharField(max_length=6,primary_key=True)
    def __str__(self):
        return self.location



    
class inventory(models.Model):

    sku=models.ForeignKey(products,on_delete=models.CASCADE)
    location=models.ForeignKey(locations,on_delete=models.CASCADE)
    amount=models.IntegerField(validators=[MinValueValidator(0,message='amount must be greater than 0')])
    available=models.IntegerField(default=-1)
    serial=models.IntegerField(unique=True,default=None,blank=True)


class newInventory(models.Model):
    sku = models.ForeignKey(products,on_delete = models.PROTECT)
    amount=models.IntegerField()
    dt=models.DateTimeField(default= datetime.now())
    user_id=models.ForeignKey(user, on_delete = models.PROTECT)

"""
class user(models.Model):
    

    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50,unique=True)
    name=models.CharField(max_length=50)
    role=models.IntegerField(choices=user_types, default=3)
    status=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} is a {self.role}"

    def role_redirect(self):
        return user_types[self.role][1]

class products(models.Model):
    
    sku=models.IntegerField(unique=True)
    name=models.CharField(max_length=50 ,unique=True)
    price=models.FloatField()
    descprition=models.CharField(max_length=200)
    category=models.IntegerField(categories)


class locations(models.Model):
        code = models.CharField(primary_key=True ,max_length=10)

class inventory(models.Model):
    sku=models.ForeignKey(products)
    location = models.ForeignKey(locations)
    amount = models.IntegerField()#
    available = models.IntegerField()#
    serial = models.IntegerField(unique=True,default=None)


class orders(models.Model): 
    create_date = models.DateTimeField(default=datetime.now()) 
    return_date = models.DateTimeField(default=datetime(create_date)) # check
    user_id = models.ForeignKey(user)
    status = models.IntegerField(choices=status, default=0)

class specific_order(models.Model): 
        order_id=models.ForeignKey(orders) 
        sku = models.IntegerField(unique=True)  
        amount = models.IntegerField()#
        inventory_id=models.ForeignKey(inventory)
        completed = models.BooleanField(default = False)


class new_inventory(models.Model):
        sku = models.ForeignKey(products)  
        amount = models.IntegerField()#
        date_time = models.DateTimeField(default=datetime.now())  
        user_id = models.ForeignKey(user)

"""