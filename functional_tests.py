#!/usr/bin/python3
# Functional tests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Listy', header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Wpisz rzecz do zrobienia'
		)

		inputbox.send_keys('Kupic pawie piora')
		inputbox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Kupic pawie piora' for row in rows)
		)
		self.fail('Zakonczenie testu!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')
