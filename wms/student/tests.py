from django.test import TestCase
from website.models import products,inventory,locations,user1,specific_order,orders
from student import function
from django.contrib.auth.models import Group


class TestWorker_function(TestCase):
    @classmethod
    def setUpTestData(cls):
        g=Group.objects.create(name='student')
        user = user1.objects.create(username= 'matan',email='matan123@gmail.com', full_name = 'matani',role = g)
        for i in range(10):
            orders.objects.create(order_number = i+1*400,user_id = user)
            
    def test_status_order(self):
        with self.subTest("Without fillter"):
            user = user1.objects.get(username= 'matan')
            self.assertEqual(len(function.getOrders({'order_number':"",'create_date':"",'create_date_end':"",'status':""},user)),10)
