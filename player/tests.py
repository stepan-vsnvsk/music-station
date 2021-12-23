from django.test import TestCase
from django.urls import reverse
from itertools import cycle

class HomePageTest(TestCase):
    pages = ["/", "/home", "/index"]
    urls = ['player:home', 'player:index']
    templates_name = ('player/index.html', 'player/base.html')    
    
    def test_page_status_code(self):
        for page in self.pages:
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertEqual(response.status_code, 200)

    def test_view_url_code_by_name(self):
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(reverse(url))
                self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for url in self.urls:
            with self.subTest(url=url):                
                response = self.client.get(reverse(url))                
                self.assertTemplateUsed(response, *self.templates_name)
