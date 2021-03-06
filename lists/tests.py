#from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.template import RequestContext
import unittest
from lists.views import home_page
from lists.models import Item
from django.test import TestCase
import re
import requests

class HomePageTest(unittest.TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def remove_csrf(html_code):
		csrf_regex = r'&lt;input[^&gt;]+csrfmiddlewaretoken[^&gt;]+&gt;'
		#csrf_regex = r’]+csrfmiddlewaretoken[^>]+>’
		print(re.sub(csrf_regex, '', html_code))
		return re.sub(csrf_regex, '', html_code)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		#self.assertEqual( self.remove_csrf(response.content.decode()), self.remove_csrf(expected_html))
		self.assertEqual(response.status_code, 200)
	
	def test_home_page_can_save_a_POST_request(self):
		self.maxDiff = None
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'Nowy element listy'
		response = home_page(request)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'Nowy element listy') 

	def test_home_page_redirects_after_a_POST_request(self):
		self.maxDiff = None
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'Nowy element listy'
		response = home_page(request)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')

	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 3)

	def test_home_page_displays_all_list_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')
		
		request = HttpRequest()
		response = home_page(request)

		self.assertIn('itemey 1', response.content.decode())
		self.assertIn('itemey 2', response.content.decode())
	

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'Absolutnie pierwszy element listy'
		first_item.save()

		second_item = Item()
		second_item.text = 'Drugi element'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(),2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
		self.assertEqual(second_saved_item.text, 'Drugi element')
