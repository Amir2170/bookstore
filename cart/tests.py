from django.test import TestCase
import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model

from .models import Cart, Item
from shop.models import Product, Category


class CartAndItemModelTest(TestCase):

	# Helper function for creating a cart
	def _create_cart_in_database(self, usr_email, usr_pass, 
		creation_date, checked_out=False):
		user = self._create_user_in_database(email=usr_email, password=usr_pass)
		cart = Cart.objects.create(user=user, creation_date=creation_date, 
			checked_out=checked_out,
		)
		return cart

	
	# Helper function for creating a user
	def _create_user_in_database(self, email, password):
		User = get_user_model()
		user = User.objects.create(email=email, password=password)
		return user

	
	# Helper function fot creating an item and its associated
	# product and category 
	def _create_item_in_database(self, cart, 
		product_name='product', category_name='category', 
		unit_price=Decimal("100")):
		category = Category.objects.create(
			name=category_name,
			slug=category_name,
			is_sub=False,
		)
		product = Product.objects.create(
			name=product_name,
			author='author',
			language='Farsi',
			slug=product_name,
			description='description',
			price=unit_price,
		)
		item = Item.objects.create(cart=cart, 
			unit_price=unit_price, object_id=product.id, 
			content_object=product,
		)
		return item


	def test_cart_creation_in_database(self):
		cart = self._create_cart_in_database(
			usr_email='testuser1@email.com',
			usr_pass='testuser1',
			creation_date=datetime.datetime.now()
		)
		
		cart_id = cart.id

		cart_from_db = Cart.objects.get(pk=cart_id)

		self.assertEqual(cart, cart_from_db)


	def test_item_creation_and_its_association_with_cart_and_product(self):
		cart = self._create_cart_in_database(
			usr_email='testuser1@email.com',
			usr_pass='testuser1',
			creation_date=datetime.datetime.now()
		)
		item = self._create_item_in_database(cart=cart,)
		product = Product.objects.get(name='product')

		item_in_cart = cart.item_set.first()
		
		# First item in cart should be equal the item we created
		self.assertEqual(item_in_cart, item)
		# Each item should have an associated product and user
		self.assertEqual(item_in_cart.cart.user.email, 'testuser1@email.com')
		self.assertEqual(item_in_cart.product.name, 'product')

		self.assertEqual(item_in_cart.unit_price, Decimal("100"))

	
	def test_cart_total_price(self):
		cart = self._create_cart_in_database(
			usr_email='testuser1@email.com',
			usr_pass='testuser1',
			creation_date=datetime.datetime.now()
		)
		
		item1 = self._create_item_in_database(cart=cart,
			unit_price=100.2, product_name='product1',
			category_name='category1',
		)
		item2 = self._create_item_in_database(cart=cart,
			unit_price=200.2, product_name='product2',
			category_name='category2',
		)

		self.assertEqual(cart.total_price, Decimal('300.4'))

	def test_item_product_update(self):
		cart = self._create_cart_in_database(
			usr_email='testuser1@email.com',
			usr_pass='testuser1',
			creation_date=datetime.datetime.now()
		)
		
		item = self._create_item_in_database(cart=cart,
			unit_price=100.2,)
		
		product1 = Product.objects.get(name='product')
		
		self.assertEqual(item.product, product1)

		product2 = Product.objects.create(
			name='product2',
			author='author',
			language='Farsi',
			slug='product2',
			description='description',
			price='100',
		)
		item.product = product2

		self.assertEqual(item.product, product2)








