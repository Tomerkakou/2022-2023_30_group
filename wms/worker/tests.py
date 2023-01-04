from django.test import TestCase
from website.models import products,inventory,locations,user1
from worker.function import getInventory,getProducts,addNewInv 
from worker import function
from worker.forms import inventoryForm
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.urls import reverse


class TestWorker_function(TestCase):
    @classmethod
    def setUpTestData(cls):
        x=locations.objects.create(location="A1")
        returns=locations.objects.create(location="RETRNS")
        for prod in range(10):
            y=products.objects.create(sku=prod,name=prod,price=10,description="csony ",category=0,serial_item=prod%2)
            inventory.objects.create(sku=y,location=x,amount=10,available=10)
        product=products.objects.create(sku=123,name='123',price=10,description="csony ",category=0,serial_item=1)
        item_to_return=inventory.objects.create(id=20,sku=product,location=returns,amount=1,available=0,serial=1234)
        

    def test_products_objects_search(self):
        with self.subTest("clear search"):
            self.assertEqual(len(getProducts({'sku':"",'name':"",'category':""})),11)
        with self.subTest("filter by one parmeters"):
            self.assertEqual(len(getProducts({'sku':"1",'name':"",'category':""})),1)
    
    def test_inventory_search(self):
        """show inventory test"""
        with self.subTest("clear search"):
            self.assertEqual(len(getInventory({'sku':"",'location_search':"",'category':"",'serial':""})),10)
        with self.subTest("filter by one sku"):
            self.assertEqual(len(getInventory({'sku':"1",'location_search':"",'category':"",'serial':""})),1)
        with self.subTest("filter by location"):
            self.assertEqual(len(getInventory({'sku':"",'location_search':"A1",'category':"",'serial':""})),10)
        with self.subTest("filter by category"):
            self.assertEqual(len(getInventory({'sku':"",'location_search':"",'category':"1",'serial':""})),0)

    def test_addInventory(self):
        g=Group.objects.create(name='test')
        form1=inventoryForm(initial={'sku':1,'location':locations.objects.get(location='A1'),'amount':10,"serial":123})
        u=user1.objects.create(username='user1',password='123',email='1@gmail.com',full_name='user',role=g)
        with self.subTest("item with serial number"):
            self.assertRaises(ValueError,addNewInv,data={'sku':'1','serial':'123','amount':2},form=form1,user=u)

    def test_return_loan(self):
        with self.subTest("succsesfull return item from loan"):
            location=locations.objects.get(location='A1')
            self.assertEqual(f'123 with serial:1234 moved to A1',function.return_item(20,location))
            item=inventory.objects.get(id=20)
            self.assertEqual(item.location.location,'A1')
            self.assertEqual(item.available,1)
        with self.subTest("Invalid inventory id"):
            self.assertEqual(None,function.return_item(-1,location))

    def change_location_test(self):
            pass
            
        
    


    # def test_excel_report_format(self):
    #     # Call the function to generate the Excel report
    #     response_to_test=HttpResponse(content_type='application/ms-excel')
    #     report = function.create_excel_for_worker(response_to_test)
        
    #     # Check that the report has the correct number of sheets
    #     self.assertEqual(len(report.sheets), 1)

    #     # Check that the first sheet has the correct column names
    #     self.assertEqual(report.sheets[0].column_names, ['ID', 'Name', 'Email'])

    #     # Check that the second sheet has the correct data types
    #     self.assertEqual(report.sheets[1].data_types, ['integer', 'string', 'email'])


