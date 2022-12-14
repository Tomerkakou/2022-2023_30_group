from django.test import TestCase
from website.models import user
from manager.function import getUsers,deleteUser

class Manager_tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(10):
            user.objects.create(username=str(i),password='1234',email=str(i)+'@gmail.com',name='user',role=i%3)

    def test_getUser(self):
        data={'username':"",'fullname':"",'email':"","role":""}
        self.assertEqual(len(getUsers(data)),10)
        data['role']="1"
        self.assertEqual(len(getUsers(data)),3)
    
    def delete_user(self):
        deleteUser('0')
        data={'username':"",'fullname':"",'email':"","role":""}
        self.assertEqual(len(getUsers(data)),9)



