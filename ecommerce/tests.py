import unittest
from django import test
from django.test import Client, SimpleTestCase
from django.test import LiveServerTestCase

from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from . import models
from time import sleep
import time
from contextlib import suppress
from django.contrib.auth.models import User

def consolify(content):
    return content.replace("\\n", "\n")

def fill_db_with_products():
    book_category_one = models.ProductCategory.objects.create(name='books_one')
    models.Product.objects.create(name='some books', description='book description', price=15, category=book_category_one)

    book_category_two = models.ProductCategory.objects.create(name='books_two')
    models.Product.objects.create(name='some another book ', description='next descriptions', price=1, category=book_category_two)


class SeleniumTest(LiveServerTestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        #self.driver.maximize_window()
        self.client = Client()
        self.EXPECTED_MAIN_TITLE = u'Ecommerce'
        #self.driver.set_window_size(1300, 550)

    def tearDown(self):
        pass

    def test_main_page(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')
        title = driver.title
        print(title)
        assert title == self.EXPECTED_MAIN_TITLE

    def test_kategorie_page(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/product_categories/')
        title = driver.title
        print(title)
        assert title == self.EXPECTED_MAIN_TITLE
        self.driver.close()

    def test_ksiazki_page(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/products/')
        title = driver.title
        print(title)
        assert title == self.EXPECTED_MAIN_TITLE
        self.driver.close()


    def create_user(self, username, password):
        self.admin = User.objects.create_superuser(username, 'email@test.com', password)
        models.Cart.objects.create(user=self.admin)

    def login_user(self, username, password):
        self.driver.get(self.live_server_url + '/admin/')
        self.driver.find_element_by_id('id_username').send_keys(username)
        el = self.driver.find_element_by_id('id_password')
        el.send_keys(password)
        el.send_keys(Keys.TAB)
        el.send_keys(Keys.RETURN)

    def assert_nothing_in_the_cart(self):
        self.assertEqual(self.driver.find_element_by_id('cart-price').text, '0$')
        self.assertEqual(self.driver.find_element_by_id('cart-items').text, '0')

    def insert_product(self):
        self.driver.find_element_by_xpath('//a[@href="/cart/add/1"]').click()
        self.driver.find_element_by_xpath('//a[@href="/cart/add/1"]').click()
        self.driver.find_element_by_xpath('//a[@href="/cart/add/2"]').click()

    def remove_first_product(self):
        self.driver.find_element_by_xpath('//a[@href="/cart/remove/1"]').click()

    def remove_second_product(self):
        self.driver.find_element_by_xpath('//a[@href="/cart/remove/2"]').click()

    def test_general(self):
        fill_db_with_products()

        username = 'aakupiec'
        password = 'qwertyasdfg'

        self.create_user(username, password)

        self.login_user(username, password)

        self.driver.get(self.live_server_url)

        self.assert_nothing_in_the_cart()

        self.driver.get(self.live_server_url + '/products')
        self.insert_product()
        self.assertEqual(self.driver.find_element_by_id('cart-price').text, '31$')
        self.assertEqual(self.driver.find_element_by_id('cart-items').text, '3')

        self.driver.get(self.live_server_url + '/cart')

        self.remove_first_product()
        self.assertEqual(self.driver.find_element_by_id('cart-price').text, '16$')
        self.remove_first_product()
        self.assertEqual(self.driver.find_element_by_id('cart-price').text, '1$')
        self.remove_second_product()
        self.assertEqual(self.driver.find_element_by_id('cart-price').text, '0$')
        self.driver.close()



class TestFacebookLoginWithSelenium(test.LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome()


    def test_if_user_logs_in(self):
        self.open_login_page()
        windows = self.driver.window_handles
        self.submit_login_form()
        time.sleep(5)


    def open_login_page(self):
        self.driver.get('http://127.0.0.1:8000/login/')
        login_link = self.driver.find_element_by_id('google_login')
        login_link.click()

    def submit_login_form(self):
        facebook_email = 'konto.moje.testowe@gmail.com'
        facebook_pass = 'qwertyasdfg'

        email = self.driver.find_element_by_id('Email')
        if email:
            email.send_keys(facebook_email)

        next = self.driver.find_element_by_id('next')
        if next:
            next.click()

        sleep(5)

        user_pass = self.driver.find_element_by_id('Passwd')
        if user_pass:
            user_pass.send_keys(facebook_pass)

        sleep(3)

        sign_in = self.driver.find_element_by_id('signIn')
        if sign_in:
            sign_in.click()

        sleep(7)

        #access = self.driver.find_element_by_id('submit_approve_access')
        #if access:
        #    access.click()

        #sleep(3)

        self.driver.close()


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
            fill_db_with_products()

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
        self.assertTrue('some books' in content)
        self.assertTrue('book description' in content)

    def test_products_when_logged_in(self):
        logged_in = self.client.login(username='user', password='password')
        self.assertTrue(logged_in)

        response = self.client.get('/products/')
        content = str(response.content)

        self.assertTrue('href="/cart/add/1"' in content)

    def test_categories(self):
        response = self.client.get('/product_categories/%s' % (models.ProductCategory.objects.get(name='books_two').id,))
        content = str(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertFalse('books_one' in content)
        self.assertTrue('books_two' in content)

    def test_categories_when_logged_in(self):
        logged_in = self.client.login(username='user', password='password')
        self.assertTrue(logged_in)

        response = self.client.get('/product_categories/%s' % (models.ProductCategory.objects.get(name='books_one').id,))
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
        self.assertTrue('some book' in content)
        self.assertTrue('some another book' in content)

        self.assertTrue('<span id="cart-price">16$</span>' in content)
        self.assertTrue('<span id="cart-items">2</span>' in content)

