from django.test import TestCase
from freezegun import freeze_time
import datetime
import tempfile
from django.contrib.auth import get_user_model

from shop.models import Category, Product, Review

User = get_user_model()


class CategoryModelTest(TestCase):

	def test_main_class_and_subclass(self):
		main_category = Category.objects.create(
			name='main_category',
			slug='main_category',
			is_sub=False,
		)
		sub_category = Category.objects.create(
			name='sub_category',
			slug='sub_category',
			is_sub=True,
			category=main_category,
		)
		self.assertEqual(sub_category.name, 'sub_category')
		self.assertEqual(sub_category.slug, 'sub_category')
		self.assertTrue(sub_category.is_sub)
		self.assertEqual(sub_category.category, main_category)

	def test_string_respresentation_of_model(self):
		category = Category.objects.create(
			name='category',
			slug='category',
			is_sub=False,
		)
		self.assertEqual(str(category), 'category')


@freeze_time('2020-12-06 07:10:23')
class ProductModelTest(TestCase):

	def test_model_fields(self):
		image = tempfile.NamedTemporaryFile(suffix='.jpg').name
		category = Category.objects.create(
			name='category',
			slug='category',
			is_sub=False,
		)
		product = Product.objects.create(
			name='category',
			author='author',
			language='Farsi',
			slug='slug',
			image=image,
			description='description',
			price=10000,
		)
		product.categories.add(category)
		self.assertEqual(product.categories.all()[0], category)
		self.assertEqual(product.name, 'category')
		self.assertEqual(product.slug, 'slug')
		self.assertEqual(product.author, 'author')
		self.assertEqual(product.language, 'Farsi')
		self.assertEqual(product.image, image)
		self.assertEqual(product.description, 'description')
		self.assertEqual(product.price, 10000)
		self.assertEqual(
			datetime.datetime.strftime(product.created, '%Y-%m-%d %H:%M:%S'),
			'2020-12-06 07:10:23'
		)
		self.assertEqual(
			datetime.datetime.strftime(product.updated, '%Y-%m-%d %H:%M:%S'),
			'2020-12-06 07:10:23'
		)


class ReviewModelTest(TestCase):

	def test_model_fields(self):
		image = tempfile.NamedTemporaryFile(suffix='.jpg').name
		category = Category.objects.create(
			name='category',
			slug='category',
			is_sub=False,
		)
		product = Product.objects.create(
			name='category',
			author='author',
			language='Farsi',
			slug='slug',
			image=image,
			description='description',
			price=10000,
		)
		user = User.objects.create_user(
			email='test@user.com',
			phone='09111111111',
			name='testuser',
		)
		review = Review.objects.create(
			product=product,
			author=user,
			review='test review',
		)
		product.categories.add(category)
		self.assertEqual(review.product, product)
		self.assertEqual(review.author, user)
		self.assertEqual(review.review, 'test review')














