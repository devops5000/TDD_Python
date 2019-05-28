#!/usr/bin/python3
# Functional tests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from django.test import LiveServerTestCase
import unittest
import time

class NewVisitorsTest(LiveServerTestCase):
	
	def setUp(self):
		self.binary = FirefoxBinary('/opt/firefox/firefox/firefox')
		self.browser = webdriver.Firefox(firefox_binary=self.binary)
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])

	def test_cat_start_a_list_and_retrive_it_later(self):
		self.browser.get(self.live_server_url)
		
		# Test uruchomionego default django
		#assert 'Django' in browser.title

		# Tytul strony
		self.assertIn('Listy', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Twoja', header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Wpisz rzeczy do zrobienia'
		)
		inputbox.send_keys('Kupic pawie piora')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(10)
		self.check_for_row_in_list_table('1: Kupic pawie piora')
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Uzyc pawich pior do zrobienia przynety')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(10)
		
		self.check_for_row_in_list_table('1: Kupic pawie piora')
		self.check_for_row_in_list_table('2: Uzyc pawich pior do zrobienia przynety')

		self.fail('Zakonczenie testu!')

