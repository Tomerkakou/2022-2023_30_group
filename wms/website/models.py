from django.db import models
from enum import Enum
from datetime import datetime, timedelta
from django.core.validators import EmailValidator , MinValueValidator
from django.contrib.auth.models import AbstractUser,Group


categories=(# update in changes in show inventory
        (0,"Photographic products"),
        (1,"Writing Tools"),)

status=( 
    (0, "waiting"),
    (1, "completed"),
    (2, "collected"),)

class user1(AbstractUser):
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=50,unique=True)
    full_name=models.CharField(max_length=50)
    role=models.ForeignKey(Group,on_delete=models.PROTECT)


class products(models.Model):
    
    sku=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50 ,unique=True)
    price=models.FloatField()
    description=models.TextField()
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
    amount=models.IntegerField(validators=[MinValueValidator(1,message='amount must be greater than 0')])
    available=models.IntegerField(default=-1)
    serial=models.IntegerField(unique=True,default=None,null=True,blank=True)

    def setAvailable(self):
        self.available=self.amount
        self.save()


class newInventory(models.Model):
    sku = models.ForeignKey(products,on_delete = models.PROTECT)
    amount=models.IntegerField()
    dt=models.DateTimeField(default= datetime.now())
    user_id=models.ForeignKey(user1, on_delete = models.PROTECT)


class orders(models.Model):
    order_number=models.AutoField(primary_key=True) 
    create_date = models.DateTimeField(default=datetime.now()) 
    return_date = models.DateTimeField(default=datetime.now()+timedelta(days=20)) 
    user_id = models.ForeignKey(user1, on_delete=models.PROTECT)
    status = models.IntegerField(choices=status, default=0)

    def return_status(self):
        return status[self.status][1]

    def str_create_date(self):
        return self.create_date.strftime("%d/%m/%Y")

    def str_return_date(self):
        return self.return_date.strftime("%d/%m/%Y")

class specific_order(models.Model): 
        order_id=models.ForeignKey(orders ,on_delete=models.CASCADE) 
        sku = models.ForeignKey(products, on_delete=models.PROTECT)  
        amount = models.IntegerField(validators=[MinValueValidator(0,message='amount must be greater than 0')])
        inventory_id=models.ForeignKey(inventory,on_delete=models.SET_NULL,null=True)
        completed = models.BooleanField(default = False)

        def getStatus(self):
            if self.completed==0:
                return 'Waiting'
            else:
                return 'Completed'




