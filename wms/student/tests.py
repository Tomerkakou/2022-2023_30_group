from django.test import TestCase
from website.models import products,inventory,locations,user1,orders,specific_order
from django.contrib.auth.models import Group
from student import function
from django.urls import reverse 

class Student_Test_function(TestCase):

    @classmethod
    def setUpTestData(cls):
        g=Group.objects.create(name='Student')
        
    def test_create_order(self):
        print("test_create_order")
        u=user1.objects.create(username='user1',password='123',email='1@gmail.com',full_name='user',role=Group.objects.create(name='test'))
        order=orders.objects.create(user_id=u)
        product1=products.objects.create(sku=820,name='820',price=10,description=" ",category=0,serial_item=0)
        product2=products.objects.create(sku=830,name='830',price=10,description=" ",category=0,serial_item=1)
        a1=locations.objects.create(location='A3')
        a2=locations.objects.create(location='A4')
        inv1=inventory.objects.create(sku=product1,location=a1,amount=20,available=20)
        data={'product':'830','amount':30}
        with self.subTest("product with no stock"):
            self.assertEqual(function.newOrder_spec(data,order),'No stock for product')
        inv2=inventory.objects.create(sku=product2,location=a2,amount=1,available=1,serial=11111)
        data['product']='820'
        with self.subTest("Not enough available form the product"):
            self.assertEqual(function.newOrder_spec(data,order),'Only 20 in stock')
        data['amount']=10
        with self.subTest("create one specific order"):
            self.assertEqual(function.newOrder_spec(data,order),"Order updated")
            self.assertEqual(specific_order.objects.filter(order_id=order).first().amount,10)
        with self.subTest("increase the amount of the specific order instead of creating new one"):
            function.newOrder_spec(data,order)
            self.assertEqual(specific_order.objects.filter(order_id=order).count(),1)
            self.assertEqual(specific_order.objects.filter(order_id=order).first().amount,20)

    def test_getOrder_history(self):
        print("test_getOrder_history")
        user=user1.objects.create(username='user1',password='123',email='1@gmail.com',full_name='user',role=Group.objects.create(name='test'))
        user2=user1.objects.create(username='user2',password='123',email='2@gmail.com',full_name='user',role=Group.objects.get(name='test'))
        orders.objects.create(user_id=user)
        data={'order_number':'','create_date':'','create_date_end':'','status':''}
        with self.subTest("user with one order"):
            self.assertEqual(function.getOrders(data,user).count(),1)
        with self.subTest("user with no orders"):
            self.assertEqual(function.getOrders(data,user2).count(),0)

    def test_get_inventory(self):
        print("test_get_inventory")
        product1=products.objects.create(sku=820,name='820',price=10,description=" ",category=0,serial_item=0)
        product2=products.objects.create(sku=830,name='830',price=10,description=" ",category=0,serial_item=1)
        a1=locations.objects.create(location='A3')
        a2=locations.objects.create(location='A4')
        inv=inventory.objects.create(sku=product1,location=a1,amount=20,available=20)
        inv2=inventory.objects.create(sku=product1,location=a2,amount=20,available=20)
        inventory.objects.create(sku=product2,location=a2,amount=1,available=1,serial=11111)
        inventory.objects.create(sku=product2,location=a1,amount=1,available=1,serial=12221)
        data={'sku':'','category':'','name':''}
        
        with self.subTest("only two result one for each item with sum of available amount"):
            result=function.sumInventory(data)
            self.assertEqual(result.count(),2)
            res1,res2=result
            self.assertEqual(res1['sum_amount'],40)
            self.assertEqual(res2['sum_amount'],2)
        with self.subTest("deacrising the available amount "):
            inv.available=0
            inv.save()
            result=function.sumInventory(data)
            self.assertEqual(result.count(),2)
            res1=result.first()
            self.assertEqual(res1['sum_amount'],20)
        with self.subTest("deacrising the available amount to 0 and getting no result for this item"):
            inv2.available=0
            inv2.save()
            result=function.sumInventory(data)
            self.assertEqual(result.count(),1)
            for res1 in result:
                self.assertNotEqual(res1['sku'],820)
            
    def test_deleteItem_and_deleteOrder(self):
        print("test_deleteItem_and_deleteOrder")
        u=user1.objects.create(username='user1',password='123',email='1@gmail.com',full_name='user',role=Group.objects.create(name='test'))
        order=orders.objects.create(user_id=u)
        product1=products.objects.create(sku=820,name='820',price=10,description=" ",category=0,serial_item=0)
        product2=products.objects.create(sku=830,name='830',price=10,description=" ",category=0,serial_item=1)
        a1=locations.objects.create(location='A3')
        a2=locations.objects.create(location='A4')
        inv1=inventory.objects.create(sku=product1,location=a1,amount=20,available=20)
        inv2=inventory.objects.create(sku=product2,location=a2,amount=1,available=1,serial=11111)
        data={'product':'820','amount':20}
        function.newOrder_spec(data,order)
        data={'product':'830','amount':1}
        function.newOrder_spec(data,order)
        with self.subTest("order created succesfully"):
            self.assertEqual(specific_order.objects.filter(order_id=order).count(),2)
        with self.subTest("delete one item"):
            function.deleteItem(820,order)
            self.assertEqual(specific_order.objects.filter(order_id=order).count(),1)
        with self.subTest("delete all the order"):
            function.deleteOrder(order.order_number)
            self.assertEqual(specific_order.objects.filter(order_id=order).count(),0)
            self.assertRaises(Exception,orders.objects.get,pK=order.order_number)
  
    """def test_status_order(self):
        print("test_status_order")
        u=user1.objects.create(username='user1',password='123',email='1@gmail.com',full_name='user',role=Group.objects.create(name='test'))
        for i in range(10):
            orders.objects.create(user_id = u)
        with self.subTest("Without fillter"):
            self.assertEqual(function.getOrders({'order_number':"",'create_date':"",'create_date_end':"",'status':""},u).count(),10)
"""
    def test_price_export(self):
        print("test_price_export")
        user1.objects.create_user(username='test',password='test',email='test@gmail.com',role=Group.objects.get(name='Student'))
        self.client.login(username='test',password='test')
        response=self.client.get(reverse('price-student-exel'))
        with self.subTest("get the correct view function"):
            self.assertEqual(response.status_code,200)
        with self.subTest("return an exel file"):
            self.assertEqual(response.get('content-type'),'application/ms-excel') 
        
    def test_recepit_export(self):
        print("test_recepit_export")
        user=user1.objects.create_user(username='test',password='test',email='test@gmail.com',role=Group.objects.get(name='Student'))
        order=orders.objects.create(user_id=user,status=2)
        self.client.login(username='test',password='test')
        response=self.client.get(reverse('receipt',args=(order.order_number,)))
        with self.subTest("get the correct view function"):
            self.assertEqual(response.status_code,200)
        with self.subTest("return an pdf file"):
            self.assertEqual(response.get('content-type'),'application/pdf') 
        with self.subTest("tests the correct file name"):
            self.assertEqual(response.get('Content-Disposition'),'inline; attachment; filename=Recepit'+str(order.order_number)+'.pdf')
        
        
        
        
      