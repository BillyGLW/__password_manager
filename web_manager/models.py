from django.db import models

# Create your models here.

class web_manager_password(models.Model):
	site_name = models.CharField(max_length = 254, verbose_name="Site name", default="django web based password manager")
	site_url = models.URLField(max_length = 200, verbose_name="Site URL")
	account_name = models.CharField(max_length = 254, verbose_name="Account name")
	account_password = models.CharField(max_length = 254, verbose_name="Account password")

	def __str__(self):
		return self.account_name


import code
dct = locals()
for k in list(globals()):
  dct[k] = globals()[k]
code.InteractiveConsole(dct).interact()
