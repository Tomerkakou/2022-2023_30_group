from django.test import TestCase
from worker.function import getInventory,getProducts,addNewInv,getOrders,getOrderlist
from website.models import products,inventory,locations,user1,orders,specific_order
from worker import function
from worker.forms import inventoryForm
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.urls import reverse 


class TestWorker_function(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        g=Group.objects.create(name='worker')

        x=locations.objects.create(location="A1")
        locations.objects.create(location="A2")
        returns=locations.objects.create(location="RETRNS")
        for prod in range(10):
            y=products.objects.create(sku=prod,name=prod,price=10,description="csony ",category=0,serial_item=prod%2)
            inventory.objects.create(sku=y,location=x,amount=10,available=10)
        product=products.objects.create(sku=123,name='123',price=10,description="csony ",category=0,serial_item=1)
        item_to_return=inventory.objects.create(id=20,sku=product,location=returns,amount=1,available=0,serial=1234)

        item=inventory.objects.create(id=19,sku=product,location=returns,amount=1,available=0,serial=134) 
        user = user1.objects.create(username= 'osnat',email='123@gmail.com', full_name = 'osnat shabtay',role = g)
        order = orders.objects.create(order_number = 1000,user_id = user)
        spe_order = specific_order.objects.create(order_id = order,sku=product,amount = 10,inventory_id = item)

        

    def test_products_objects_search(self):
        print('test_products_objects_search')
        with self.subTest("clear search"):
            self.assertEqual(len(getProducts({'sku':"",'name':"",'category':""})),11)
        with self.subTest("filter by one parmeters"):
            self.assertEqual(len(getProducts({'sku':"1",'name':"",'category':""})),1)
    
    def test_inventory_search(self):
        """show inventory test"""
        print('test_inventory_search')
        with self.subTest("clear search"):
            self.assertEqual(len(getInventory({'sku':"",'location_search':"",'category':"",'serial':""})),10)
        with self.subTest("filter by one sku"):
            self.assertEqual(len(getInventory({'sku':"1",'location_search':"",'category':"",'serial':""})),1)
        with self.subTest("filter by location"):
            self.assertEqual(len(getInventory({'sku':"",'location_search':"A1",'category':"",'serial':""})),10)
        with self.subTest("filter by category"):
            self.assertEqual(len(getInventory({'sku':"",'location_search':"",'category':"1",'serial':""})),0)

    def test_addInventory(self):
        print("test_addInventory")
        g=Group.objects.create(name='test')
        form1=inventoryForm(initial={'sku':1,'location':locations.objects.get(location='A1'),'amount':10,"serial":123})
        u=user1.objects.create(username='user1',password='123',email='1@gmail.com',full_name='user',role=g)
        with self.subTest("item with serial number"):
            self.assertRaises(ValueError,addNewInv,data={'sku':'1','serial':'123','amount':2},form=form1,user=u)

    def test_return_loan(self):
        print("test_return_loan")
        with self.subTest("succsesfull return item from loan"):
            location=locations.objects.get(location='A1')
            self.assertEqual(f'123 with serial:1234 moved to A1',function.return_item(20,location))
            item=inventory.objects.get(id=20)
            self.assertEqual(item.location.location,'A1')
            self.assertEqual(item.available,1)
        with self.subTest("Invalid inventory id"):
            self.assertEqual(None,function.return_item(-1,location))

    def test_get_orders(self):
        with self.subTest("Wthout fillter"):
            self.assertEqual(len(getOrders({'order_number':"",'create_date':"",'create_date_end':"",'status':""})),1)
    
    def test_get_order_list(self):
            with self.subTest("same msg"):
                order = orders.objects.get(order_number = 1000)
                list_specific_order = getOrderlist(order)
                self.assertEqual(len(list_specific_order),1)
                self.assertEqual(list_specific_order[0].amount,10)


    def change_location_test(self):
            print("change_location_test")
            with self.subTest("succsesfull change inventory location"):
                self.assertEqual(function.move_to(20,'A2'),'item: 123 moved to A2')
                item=inventory.objects.get(id=20)
                self.assertEqual(item.location.location,'A2')
            with self.subTest("merge two inventory when one is moved to the others location from same product"):
                product=products.objects.create(sku=790,name='790',price=10,description=" ",category=0,serial_item=0)
                a1=locations.objects.get(location='A1')
                a2=locations.objects.get(location='A2')
                inventory.objects.create(id=30,sku=product,location=a1,amount=10,available=10)
                inventory.objects.create(id=40,sku=product,location=a2,amount=10,available=10)
                self.assertEqual(function.move_to(30,'A2'),'item: 790 moved to A2')
                self.assertEqual(inventory.objects.get(id=40).amount,20)
                self.assertRaises(Exception,inventory.objects.get,id=30)
            with self.subTest("Invalid inventory id or location"):
                self.assertEqual(function.move_to(50,'A2'),None)
                self.assertEqual(function.move_to(40,'A'),None)

    def complete_order_test(self):
        print("complete_order_test")
        u=user1.objects.create(username='user1',password='123',email='1@gmail.com',full_name='user',role=Group.objects.create(name='test'))
        order=orders.objects.create(order_number=10,user_id=u)
        product1=products.objects.create(sku=800,name='800',price=10,description=" ",category=0,serial_item=0)
        product2=products.objects.create(sku=810,name='810',price=10,description=" ",category=0,serial_item=1)
        a1=locations.objects.get(location='A1')
        a2=locations.objects.get(location='A2')
        inv1=inventory.objects.create(id=90,sku=product1,location=a1,amount=10,available=5)
        inv2=inventory.objects.create(id=100,sku=product2,location=a2,amount=1,available=0,serial=1212)
        specific_order.objects.create(id=9,order_id=order,sku=product1,amount=5,inventory_id=inv1)
        specific_order.objects.create(id=10,order_id=order,sku=product2,amount=1,inventory_id=inv2)
        with self.subTest("order status,return date"):
            self.assertEqual(order.status,0)
            self.assertEqual(order.return_date,None)
        with self.subTest("after completing part of the order status change"):
            self.assertEqual(function.completeOrder_list((9,),order),1)
            self.assertEqual(specific_order.objects.get(id=9).completed,True)
            self.assertEqual(inventory.objects.get(id=90).amount,5)
        with self.subTest("after completing all of the order status change"):
            self.assertEqual(function.completeOrder_list((10,),order),2)
            self.assertEqual(specific_order.objects.get(id=10).completed,True)
            inv=inventory.objects.get(id=100)
            self.assertEqual(inv.location.location,'RETRNS')
            with self.subTest("order got new return date after completed"):
                self.assertNotEqual(orders.objects.get(pK=10).return_date,None)

    



