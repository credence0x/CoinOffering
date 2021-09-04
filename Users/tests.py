from django.test import TestCase


# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse


class UserTestCase(TestCase):
		
	def test_GET_sign_in_controller(self):
		c = Client()
		res = c.get(reverse("Users:sign-in"))
		self.assertEqual(res.status_code,200)

	def test_POST_sign_in_controller(self):
		c = Client()
		res = c.post(reverse("Users:sign-in"),{'email':"lojetokun@gmail.com",
				        				'password':"verySimple",
				      				  })
		self.assertEqual(res.status_code,302)

	def test_GET_sign_up_controller(self):
		c = Client()
		res = c.get(reverse("Users:sign-up"))
		self.assertEqual(res.status_code,200)

	def test_POST_sign_up_controller(self):
		c = Client()
		res = c.post(reverse("Users:sign-up"),{'username':'username123',
			        						'password':'passwordTT123',
			        						'password2':'passwordTT123',#confirm password
			      				  			'first_name':'first_name',
			        						'last_name':'last_name',
			        						'email':'email@emailer.com'})
		self.assertEqual(res.status_code,302)

	def test_GET_home_page_controller(self):
		c = Client()
		c.login(username='lanre', password='verySimple')
		res = c.get(reverse("Users:home-page"))
		self.assertEqual(res.status_code,200)

	def test_GET_log_out_controller(self):
		c = Client()
		c.login(username='lanre', password='verySimple')
		res = c.get(reverse("Users:log-out"))
		self.assertEqual(res.status_code,302)


