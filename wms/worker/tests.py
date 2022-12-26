from django.test import TestCase
from website.models import products,inventory,locations,user1
from worker.function import getInventory,getProducts,addNewInv
from worker.forms import inventoryForm
from django.contrib.auth.models import Group

class TestWorker_function(TestCase):
    @classmethod
    def setUpTestData(cls):
        x=locations.objects.create(location="A1")
        for prod in range(10):
            y=products.objects.create(sku=prod,name=prod,price=10,description="csony ",category=0,serial_item=prod%2)
            inventory.objects.create(sku=y,location=x,amount=10,available=10)
        

    def test_products_objects_search(self):
        with self.subTest("clear search"):
            self.assertEqual(len(getProducts({'sku':"",'name':"",'category':""})),10)
        with self.subTest("filter by one parmeters"):
            self.assertEqual(len(getProducts({'sku':"1",'name':"",'category':""})),1)
    
    def test_inventory_search(self):
        """show inventory test"""
        with self.subTest("clear search"):
            self.assertEqual(len(getInventory({'sku':"",'location':"",'category':"",'serial':""})),10)
        with self.subTest("filter by one sku"):
            self.assertEqual(len(getInventory({'sku':"1",'location':"",'category':"",'serial':""})),1)
        with self.subTest("filter by location"):
            self.assertEqual(len(getInventory({'sku':"",'location':"A1",'category':"",'serial':""})),10)
        with self.subTest("filter by category"):
            self.assertEqual(len(getInventory({'sku':"",'location':"",'category':"1",'serial':""})),0)

    def test_addInventory(self):
        g=Group.objects.create(name='test')
        form1=inventoryForm(initial={'sku':1,'location':locations.objects.get(location='A1'),'amount':10,"serial":123})
        u=user1.objects.create(username='user1',password='123',email='1@gmail.com',full_name='user',role=g)
        with self.subTest("item with serial number"):
            self.assertRaises(ValueError,addNewInv,data={'sku':'1','serial':'123','amount':2},form=form1,user=u)


