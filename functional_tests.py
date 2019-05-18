#!/usr/bin/python3
# Functional tests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unittest

class NewVisitorsTest(unittest.TestCase):
	
	def setUp(self):
		self.binary = FirefoxBinary('/opt/firefox/firefox/firefox')
		self.browser = webdriver.Firefox(firefox_binary=self.binary)
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_cat_start_a_list_and_retrive_it_later(self):
		self.browser.get('http://localhost:8000')
		
		# Test uruchomionego default django
		#assert 'Django' in browser.title

		# Tytul strony
		self.assertIn('Listy', self.browser.title)
		self.fail('Zakonczenie testu!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')
