import unittest
from django.test import Client
from django.contrib.auth import get_user_model

from . import models

def consolify(content):
    return content.replace("\\n", "\n")

class HomePageTest(unittest.TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('/')
        content = str(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Zaloguj' in content)

class ProductsTest(unittest.TestCase):
    @classmethod
    def setUpModels(cls):
        if not hasattr(cls, 'models_setted_up'):
            cls.models_setted_up = True
            things_category = models.ProductCategory.objects.create(name='things')
            models.Product.objects.create(name='a stick', description='for sticking purposes', price=1, category=things_category)

            fruits_category = models.ProductCategory.objects.create(name='fruits')
            models.Product.objects.create(name='an apple', description='tasty one', price=1, category=fruits_category)

            User = get_user_model()
            user = User.objects.create_user('user', password='password')
            models.Cart.objects.create(user=user)

    def setUp(self):
        self.client = Client()
        ProductsTest.setUpModels()

    def test_products(self):
        response = self.client.get('/products/')
        content = str(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('a stick' in content)
        self.assertTrue('for sticking purposes' in content)

    def test_products_when_logged_in(self):
        logged_in = self.client.login(username='user', password='password')
        self.assertTrue(logged_in)

        response = self.client.get('/products/')
        content = str(response.content)

        self.assertTrue('href="/cart/add/1"' in content)

    def test_categories(self):
        response = self.client.get('/product_categories/%s' % (models.ProductCategory.objects.get(name='fruits').id,))
        content = str(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertFalse('a stick' in content)
        self.assertTrue('an apple' in content)

    def test_categories_when_logged_in(self):
        logged_in = self.client.login(username='user', password='password')
        self.assertTrue(logged_in)

        response = self.client.get('/product_categories/%s' % (models.ProductCategory.objects.get(name='things').id,))
        content = str(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('href="/cart/add/1"' in content)

    def buy_some_products(self):
        self.client.get('/cart/add/1', follow=True)
        self.client.get('/cart/add/2', follow=True)

    def remove_products(self):
        items = models.CartItem.objects.filter(cart__user__password='password')
        [self.client.get('/cart/remove/%s' % (item.id,), follow=True) for item in items]

    def test_cart(self):
        logged_in = self.client.login(username='user', password='password')
        self.assertTrue(logged_in)

        self.buy_some_products()
        response = self.client.get('/cart', follow=True)
        content = str(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('apple' in content)
        self.assertTrue('stick' in content)

        self.assertTrue('<span id="cart-price">2$</span>' in content)
        self.assertTrue('<span id="cart-items">2</span>' in content)
