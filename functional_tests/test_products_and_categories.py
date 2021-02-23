import tempfile
import time
from selenium.common.exceptions import NoSuchElementException

from ._base import FunctionalTests
from shop.models import Category, Product, Review


class ProductCategoryTest(FunctionalTests):

	def setUp(self):
		image = tempfile.NamedTemporaryFile(suffix='.jpg').name
		main_category = Category.objects.create(
			name='main_category',
			slug='main_category',
			is_sub=False,
		)
		sub_category = Category.objects.create(
			name='sub_category',
			slug='sub_category',
			is_sub=True,
			category=main_category
		)
		product = Product.objects.create(
			name='django for beginners',
			language='En',
			author='william s',
			slug='django for beginners',
			image=image,
			description='description',
			price=10000,
		)
		product.categories.add(main_category,
			sub_category
		)
		review = Review.objects.create(
			product=product,
			review='my review',
		)
		super().setUp()

	def check_element_does_not_exist(self, locator):
		with self.assertRaises(NoSuchElementException):
			self.browser.find_element_by_xpath(f'{{locator}}')


	def test_product_and_product_detail(self):
		# User goes to the home page 
		self.browser.get(self.live_server_url)

		# He sees a product and click on its link
		self.browser.find_element_by_link_text('django for beginners').click()

		# He sees the product name, price up in a header
		product_name = self.browser.find_element_by_tag_name('h5').text
		self.wait_for(lambda:self.assertEqual(product_name, 'django for beginners'))
		self.wait_for(lambda:self.assertEqual(
			self.browser.find_element_by_id('price').text,
			'10000 T'
		))
		# He then sees product description down below
		self.wait_for(lambda:self.assertEqual(
			self.browser.find_element_by_id("name").text, 
			"django for beginners"
		))
		self.wait_for(lambda:self.assertEqual(
			self.browser.find_element_by_id("language").text, 
			'En'
		))
		self.wait_for(lambda:self.assertEqual(self.browser.find_element_by_id("author").text, 
			"william s"
		))
		self.wait_for(lambda:self.assertEqual(self.browser.find_element_by_id("available").text,
			'موجود'
		))

		# and under the big image of the product he sees comments!!!!
		self.wait_for(lambda:self.assertEqual(
			self.browser.find_element_by_id("comment").text,
			'"my review"',
		))

		# he also sees catgories that the product belongs to
		self.browser.find_element_by_link_text('main_category').click()
		self.wait_for(lambda:self.browser.find_element_by_link_text('main_category'))
		self.wait_for(lambda:self.browser.find_element_by_link_text('sub_category'))

		self.browser.find_element_by_link_text('sub_category').click()
		self.wait_for(lambda:self.browser.find_element_by_link_text('sub_category'))
		self.wait_for(lambda:self.check_element_does_not_exist('//div[@class="list-group"]/a[2]'))

		# Sure enough he goes back to the home page
		self.browser.find_element_by_link_text('21Bookstore').click()
		self.wait_for(lambda:self.browser.find_element_by_link_text('django for beginners'))

