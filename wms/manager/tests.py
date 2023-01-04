from django.test import TestCase
from website.models import user1,inventory,products,locations
from manager.function import getUsers,deleteUser,updateAmount
from django.contrib.auth.models import Group
from django.http import Http404

class Manager_tests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        g=Group.objects.create(name='test')
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
    
    def delete_user(self):
        print("delete_user")
        deleteUser('0')
        data={'username':"",'fullname':"",'email':"","role":""}
        self.assertEqual(len(getUsers(data)),9) 
    
    def update_amount_test(self): 
        print("update_amount_test")
        loc = locations.objects.get(location="123456") 
        item = products.objects.get(sku=1234)
        inv=inventory.objects.create(id=1,sku=item,location=loc,amount=50,available=20)
        with self.subTest("available amount - greater than new amount"):
            self.assertEqual(updateAmount(1,10),"#The new amount does not match the quantity ordered")
        with self.subTest("good updated amount"):
            self.assertEqual(updateAmount(1,30),f"#{inv.sku.name} in {inv.location} updated to 30")


        

        




