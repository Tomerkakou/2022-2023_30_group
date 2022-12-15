from django.test import TestCase
from website.models import user,inventory,products,locations
from manager.function import getUsers,deleteUser,updateAmount


class Manager_tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(10):
            user.objects.create(username=str(i),password='1234',email=str(i)+'@gmail.com',name='user',role=i%3)
        locations.objects.create(location="123456")
        products.objects.create(sku=1234,price=150,description="test item",name="test", category=1,serial_item=0) 
         
        

    def test_getUser(self):
        data={'username':"",'fullname':"",'email':"","role":""}
        self.assertEqual(len(getUsers(data)),10)
        data['role']="1"
        self.assertEqual(len(getUsers(data)),3)
    
    def delete_user(self):
        deleteUser('0')
        data={'username':"",'fullname':"",'email':"","role":""}
        self.assertEqual(len(getUsers(data)),9) 
    
    def update_amount_test(self): 
        loc = locations.objects.get(location="123456") 
        item = products.objects.get(sku=1234)
        inventory.objects.create(sku=item,location=loc,amount=50,available=20)
        with self.subTest("available amount - greater than new amount"):
            self.assertEqual(updateAmount(0,10),"#The new amount does not match the quantity ordered")
        with self.subTest("good updated amount"):
            self.assertEqual(updateAmount(0,20),"#{inv.sku.name} in {inv.location} updated to 20")
        with self.subTest("exception with invalid inventory id"):
            self.assertRaises(Exception,updateAmount,1,2)

        

        




