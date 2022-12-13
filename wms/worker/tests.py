from django.test import TestCase
from website.models import products,inventory
from worker.function import getInventory

class TestWorker_function(TestCase):
    
    def test_inventory_objects_search(self):
        with self.subTest("clear search"):
            self.assertEqual(len(getInventory({'sku':"",'location':"",'serial':"",'category':""})),len(inventory.objects.all()))
        with self.subTest("filter by two parmeters"):
            self.assertEqual(len(getInventory({'sku':"",'location':"A50262",'serial':"",'category':"0"})),len(inventory.objects.filter(location='A50262', category="0")))

    def test_products_objects_search(self):
        with self.subTest("clear search"):
            self.assertEqual(getInventory({'sku':"",'name':"",'category':""}),products.objects.all())
        with self.subTest("filter by two parmeters"):
            self.assertEqual(len(getInventory({'sku':"",'name':"e",'category':"0"})),len(products.objects.filter(location='A50262', category="0")))


