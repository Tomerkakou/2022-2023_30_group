from django.test import TestCase
from website.models import user1,products,locations
from django.contrib.auth.models import Group
from website.function import register,login

# Create your tests here.

class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        g=Group.objects.create(name='test')
        user1.objects.create_user(username='matan1', password='1234', email='matan@gmail.com', full_name='matan', role=g)
        user1.objects.create_user(username='osnat1', password='12345', email='os@gmail.com', full_name='osnat' ,role=g)
        products.objects.create(sku = 1234, name= 'pencill', price= 50, description = 'pink pen do something',category = 0, serial_item=0)
        locations.objects.create(location = 'A50362')
        

    def test_student_register(self):
        matan={'reg_username':'','reg_pass':'1234','reg_name':'matan','reg_email':'matan@gmail.com'}
        self.assertEqual(register(matan),"Not all details have been filled in") 
        matan={'reg_username':'matan1','reg_pass':'1234','reg_name':'matan','reg_email':'matan@gmail.com'}
        self.assertEqual(register(matan),"Username or Email already in use")  


    def test_products(self):    
        with self.subTest("checks product to str"):
            pen = products.objects.get(name = 'pencill')
            self.assertEqual(pen.__str__(),'1234-pencill')
        with self.subTest("checks return category"):
            pen = products.objects.get(name = 'pencill')
            self.assertEqual(pen.return_category(),'Photographic products')
        with self.subTest("checks succsesfull creation of new product"):
            compare=products.objects.get(name='pencill')
            pro=products.objects.create(sku = 1234567, name= 'pencill123', price= 50, description = 'pink pen do something',category = 0, serial_item=0)
            self.assertEqual(type(pro),type(compare))
        with self.subTest("checks for error when creating new product with excisting sku"):
            self.assertRaises(Exception,products.objects.create,sku = 1234, name= 'notebook', price= 50, description = 'pink notebook do something',category = 0, serial_item=0)

    def test_manager_locations(self):
        with self.subTest("checks get location and return as string"):
            check_location = locations.objects.get(location = 'A50362')
            self.assertEqual(check_location.__str__(),"A50362")  
        with self.subTest("checks error when creating new location with new id"):
            self.assertRaises(Exception,products.objects.create,'A50362')
        with self.subTest("checks succsesfull creation of new locatio "):
            loc=locations.objects.get(location='A50362')
            new=locations.objects.create(location='A12345')
            self.assertEqual(type(loc),type(new))
    
    def test_login(self):
        data={'username':'matan1','password':'1234'}
        self.assertEqual(login(data),user1.objects.get(username='matan1'))
        data={'username':'matan1','password':'invaild'}
        self.assertEqual(login(data),None) 
        data={'username':'matan1234','password':'1234'}
        self.assertEqual(login(data),None)    

    





