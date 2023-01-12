from django.test import TestCase
from website.models import user1,inventory,products,locations
from manager.function import getUsers,deleteUser,updateAmount
from django.contrib.auth.models import Group
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
            result=updateAmount(1,10)
            self.assertEqual(result[0],"#The new amount does not match the quantity ordered")
            self.assertEqual(result[1],'red')
        with self.subTest("good updated amount"):
            result=updateAmount(1,30)
            self.assertEqual(result[0],f"#{inv.sku.name} in {inv.location} updated to 30")
            self.assertEqual(result[1],'blue')

    def test_inventory_export(self):
        print("test_inventory_export")
        user1.objects.create_user(username='test',password='test',email='test@gmail.com',role=Group.objects.get(name='Manager'))
        self.client.login(username='test',password='test')
        response=self.client.get(reverse('inventory-exel'))
        with self.subTest("get the correct view function"):
            self.assertEqual(response.status_code,200)
        with self.subTest("return an exel file"):
            self.assertEqual(response.get('content-type'),'application/ms-excel')

    
    def test_lending_products_export(self):
        print("test_lending_products_export")
        user1.objects.create_user(username='test',password='test',email='test@gmail.com',role=Group.objects.get(name='Manager'))
        self.client.login(username='test',password='test')
        response=self.client.get(reverse('lendings_to_excel_for_manger'))
        with self.subTest("get the correct view function"):
            self.assertEqual(response.status_code,200)
        with self.subTest("return an exel file"):
            self.assertEqual(response.get('content-type'),'application/ms-excel')


    def test_entry_products_export(self):
        print("test_entry_products_export")
        user1.objects.create_user(username='test',password='test',email='test@gmail.com',role=Group.objects.get(name='Manager'))
        self.client.login(username='test',password='test')
        response=self.client.get(reverse('report_entry_products'))
        with self.subTest("get the correct view function"):
            self.assertEqual(response.status_code,200)
        with self.subTest("return an exel file"):
            self.assertEqual(response.get('content-type'),'application/ms-excel')



        




