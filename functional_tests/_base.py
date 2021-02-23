from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time

MAX_TIME = 10


class FunctionalTests(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()


	def tearDown(self):
		self.browser.quit()

	def wait(fn):
		def modified_fn(*args, **kwargs):
			start_time = time.time()
			
			while True:
				
				try:
					return fn(*args, **kwargs)
				
				except(WebDriverException, AssertionError, NoSuchElementException) as e:
					if time.time() - start_time > MAX_TIME:
						raise e
					time.sleep(0.5)

		return modified_fn

	@wait
	def wait_for(self, fn):
		return fn()