from django.test import TestCase
from django.test.client import Client

from .views import encrypt_password, decrypt_password
from .models import web_manager_password

from django.contrib.auth.models import User

from django.urls  import reverse

class Password_Web_Manger_TestCase(TestCase):

	def setUp(self):
		self.c = Client()

	def test_password_web_manager_redirect(self):
		"check that the PM redirects to install page when there is no PM installed"
		response = self.c.get(reverse("web_manager:index"))
		self.assertEqual(response.status_code, 200)



class Password_Web_Manager_Views_TestCase(TestCase):

	def setUp(self):
		self.c = Client()

	def test_password_web_manager_crypt_encrypt(self):
		testdata = encrypt_password("test123")
		self.assertEqual("test123", decrypt_password(testdata)) 


class Password_Web_Manager_Entry_TestCase(TestCase):

	def setUp(self):
		self.c = Client()

		for i in range(1, 2+1):
			self.user = User.objects.create_user(username="test{}".format(i), password="test")
			self.user.is_staff = True
			self.user.save()

	def test_user_entries_as_superuser(self):
		
		self.pm1 = web_manager_password(account_name="test1", account_password="abcdefgh")
		self.pm1.save()
		self._pm1 = web_manager_password(account_name="test1", account_password="AAABBB")
		self._pm1.save()

		self.pm2 = web_manager_password(account_name="test2", account_password="abcdefgh")
		self.pm2.save()

		result = web_manager_password.objects.all().filter(account_name=self.pm1.account_name)

		self.assertEqual(list(result.values('account_name')), 
		[{'account_name': self.pm1.account_name}, {'account_name': self.pm1.account_name}])

		self.assertEqual(list(result.values('account_password')), 
		[{'account_password': self.pm1.account_password}, {'account_password': self._pm1.account_password}])
