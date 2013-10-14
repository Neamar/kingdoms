# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from kingdom.models import Kingdom


class ApiTest(TestCase):
	"""
	API tests for kingdom projects.
	This is not complete. It only checks the main api returns, and does not check the other API endpoints.

	The rationale here is the endpoints only do glue code, and all the logic is done at the signal level.
	"""

	def setUp(self):
		self.u = User(username="test")
		self.u.set_password("pwd")
		self.u.save()

		self.k = Kingdom(user=self.u)
		self.k.save()

		self.c = Client()
		self.c.login(username=self.u.username, password="pwd")

	def test_api_is_up(self):
		"""
		Check API calls returns with status 200
		"""

		r = self.c.get(reverse('kingdom.views.api.api'))
		self.assertEqual(200, r.status_code)


class ViewTest(TestCase):
	"""
	Views tests for kingdom projects.
	This is not complete. It only checks the return code.
	"""

	def setUp(self):
		self.u = User(username="test")
		self.u.set_password("pwd")
		self.u.save()

		self.k = Kingdom(user=self.u)
		self.k.save()

		self.c = Client()
		self.c.login(username=self.u.username, password="pwd")

	def test_app_require_login(self):
		"""
		Check app returns with status 200
		"""

		r = Client().get(reverse('kingdom.views.index.app'))
		self.assertEqual(302, r.status_code)

	def test_login_is_up(self):
		"""
		Check app returns with status 200
		"""

		r = self.c.get(reverse('django.contrib.auth.views.login'))
		self.assertEqual(200, r.status_code)

	def test_app_is_up(self):
		"""
		Check app returns with status 200
		"""

		r = self.c.get(reverse('kingdom.views.index.app'))
		self.assertEqual(200, r.status_code)

	def test_dependencies_is_up(self):
		"""
		Check app returns with status 200
		"""

		r = self.c.get(reverse('kingdom.views.index.app'))
		self.assertEqual(200, r.status_code)
