import time

from ._base import FunctionalTests
from shop.models import Category


class HomePageTest(FunctionalTests):

	def test_home_page_title_test(self):
		self.browser.get(self.live_server_url)
		title = self.browser.find_element_by_class_name('navbar-brand').text
		self.wait_for(lambda:self.assertEqual(title, '21Bookstore'))
		name = self.browser.find_element_by_class_name('my-4').text
		self.wait_for(lambda:self.assertEqual(name, '21Bookstore'))
		self.wait_for(lambda:self.browser.find_element_by_link_text('درباره'))
		self.wait_for(lambda:self.browser.find_element_by_link_text('تماس با ما'))
