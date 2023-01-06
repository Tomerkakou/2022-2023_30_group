from django.test import TestCase
from website.models import user1,inventory,products,locations
from manager.function import getUsers,deleteUser,updateAmount
from django.contrib.auth.models import Group
from django.http import Http404
from django.urls import reverse 

class Manager_tests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        g=Group.objects.create(name='Manager')
        for i in range(10):
            user1.objects.create(username=str(i),password='1234',email=str(i)+'@gmail.com',full_name='user',role=g)
        locations.objects.create(location="123456")
        products.objects.create(sku=1234,price=150,description="test item",name="test", category=1,serial_item=0) 
    
    def test_getUser(self):
        print("test_getUser")
        data={'username':"",'fullname':"",'email':"","role":""}
        self.assertEqual(len(getUsers(data)),10)
        data['role']="1"
        self.assertEqual(len(getUsers(data)),10)
        data['role']="0"
        self.assertEqual(len(getUsers(data)),0)
    
    def test_delete_user(self):
        print("test_delete_user")
        deleteUser('0')
        data={'username':"",'fullname':"",'email':"","role":""}
        self.assertEqual(len(getUsers(data)),9)
    
    def test_update_amount(self): 
        print("test_update_amount")
        loc = locations.objects.get(location="123456") 
        item = products.objects.get(sku=1234)
        inv=inventory.objects.create(id=1,sku=item,location=loc,amount=50,available=20)
        with self.subTest("available amount - greater than new amount"):
            self.assertEqual(updateAmount(1,10),"#The new amount does not match the quantity ordered")
        with self.subTest("good updated amount"):
            self.assertEqual(updateAmount(1,30),f"#{inv.sku.name} in {inv.location} updated to 30")

    def test_inventory_export(self):
        print("test_inventory_export")
        user1.objects.create_user(username='test',password='test',email='test@gmail.com',role=Group.objects.get(name='Manager'))
        self.client.login(username='test',password='test')
        response=self.client.get(reverse('inventory-exel'))
        with self.subTest("get the correct view function"):
            self.assertEqual(response.status_code,200)
        with self.subTest("return an exel file"):
            self.assertEqual(response.get('content-type'),'application/ms-excel')

        

        




