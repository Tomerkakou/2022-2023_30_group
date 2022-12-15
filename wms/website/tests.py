from django.test import TestCase
from website.models import user,products,locations
from website.function import register,login

# Create your tests here.

class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        user.objects.create(username='matan1', password='1234', email='matan@gmail.com', name='matan', role=1, status=True)
        user.objects.create(username='osnat1', password='12345', email='os@gmail.com', name='osnat', role=2, status=False)
        products.objects.create(sku = 1234, name= 'pencill', price= 50, descprition = 'pink pen do something',category = 0, serial_item=0)
        locations.objects.create(location = 'A50362')
        
    def test_users_role(self):
        matan=user.objects.get(name='matan')
        osnat=user.objects.get(name='osnat')
        self.assertEqual(matan.get_role(),'worker')
        self.assertEqual(osnat.get_role(),'student')

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

    def test_manager_locations(self):
        check_location = locations.objects.get(location = 'A50362')
        self.assertEqual(check_location.__str__(),"A50362")  
    
    def test_login(self):
        data={'username':'matan1','password':'1234'}
        self.assertEqual(login(data),user.objects.get(username='matan1'))
        data={'username':'matan1','password':'invaild'}
        self.assertEqual(login(data),None) 
        data={'username':'matan1234','password':'1234'}
        self.assertEqual(login(data),None)    

    





