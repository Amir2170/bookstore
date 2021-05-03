from django.test import TestCase
import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model

from cart.models import Cart
from shop.models import Product, Category


class CartModelTest(TestCase):

	def _create_product_and_category_in_database(self, product_name,
        price=100):
		category = Category.objects.create(
			name='category',
			slug=product_name + 'category',
			is_sub=False,
		)
		product = Product.objects.create(
			name=product_name,
			author='author',
			language='Farsi',
			slug=product_name,
			description='description',
			price=price,
		)
		product.categories.add(category)

		return product

  
	def _create_cart_in_database(self, usr_email, usr_pass, 
		creation_date, checked_out=False):
		user = self._create_user_in_database(email=usr_email, password=usr_pass)
		cart = Cart.objects.create(user=user, creation_date=creation_date, 
			checked_out=checked_out,
		)
		return cart


	def _create_user_in_database(self, email, password):
		User = get_user_model()
		user = User.objects.create(email=email, password=password)
		return user


	def test_cart_creation_in_database(self):
		cart = self._create_cart_in_database(
			usr_email='testuser1@email.com',
			usr_pass='testuser1',
			creation_date=datetime.datetime.now()
		)
		
		cart_id = cart.id

		cart_from_db = Cart.objects.get(pk=cart_id)

		self.assertEqual(cart, cart_from_db)

	
	def test_adding_product_to_cart(self):
		cart = self._create_cart_in_database(
			usr_email='testuser1@email.com',
			usr_pass='testuser1',
			creation_date=datetime.datetime.now()
		)
		product1 = self._create_product_and_category_in_database(
			product_name='product1',
		)
		product2 = self._create_product_and_category_in_database(
			product_name='product2',
		)
		cart.products.add(product1)
		cart.products.add(product2)
		
		self.assertEqual(cart.products.get(name='product1'), 
                   product1
        )
		self.assertEqual(cart.products.get(name='product2'), 
                   product2
        )

  
	def test_cart_total_price(self):
		cart = self._create_cart_in_database(
			usr_email='testuser1@email.com',
			usr_pass='testuser1',
			creation_date=datetime.datetime.now()
		)
		
		product1 = self._create_product_and_category_in_database(
			product_name='product1', price=202.2
		)
		product2 = self._create_product_and_category_in_database(
			product_name='product2', price=300
		)
		cart.products.add(product1)
		cart.products.add(product2)

		self.assertEqual(cart.total_price, Decimal('502.2'))








