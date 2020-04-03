from django.test import TestCase
from django.test.client import Client


from django.urls  import reverse

class Password_Manager_CryptoTestCase(TestCase):

	def setUp(self):
		self.c = Client()

	def test_password_manager_redirect(self):
		''' since pm is on TODO list it should always return 302 '''
		response = self.c.get(reverse("rrol"))
		# self.assertEqual(response.status_code, 404)
		self.assertEqual(response.status_code, 302)

