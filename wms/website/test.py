from django.test import TestCase
from website.models import user,products,locations
from website.function import register
import unittest
# Create your tests here.

class TestModels(unittest.TestCase):
    def test_user (self):
        user.objects.create(username='matan1', password='1234', email='matan@gmail.com', name='matan', role=1, status=True)
        user.objects.create(username='osnat1', password='12345', email='os@gmail.com', name='osnat', role=2, status=False)
    def test_users_role(self):
        matan=user.objects.get(name='matan')
        osnat=user.objects.get(name='osnat')
        self.assertEqual(matan.get_role(),'worker')
        self.assertEqual(osnat.get_role(),'student')
    def test_users_username(self):
        matan=user.objects.get(name='matan')
        self.assertEqual(register(matan),"Username or Email already in use")  

    def test_products(self):   
        products.objects.create(sku = 1234, name= 'pencill', price= 50, descprition = 'pink pen do something',category = 0, serial_item=0)
        def test_sku_name(self): 
            pen = products.objects.get(name = 'pencill')
            self.assertEqual(pen.__str__(),'1234--pencill')
        def test_category(self): 
            pen = products.objects.get(name = 'pencill')
            self.assertEqual(pen.return_category(),'Photographic products')

    def test_locations(self):
        # locations.objects.create(location = 'A50362') 
        check_location = locations.objects.get(location = 'A50362')
        self.assertEqual(check_location.__str__(),"A50362")  







if __name__ == '__main__':
    unittest.main()


