# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.contrib.auth.models import User

from kingdom.models import Kingdom, Quality, QualityCategory

@override_settings(PASSWORD_HASHERS = ('django.contrib.auth.hashers.SHA1PasswordHasher',))
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

	def test_errors_require_enabling(self):
		"""
		Check app returns with status 200
		"""

		r = self.c.get(reverse('kingdom.views.index.errors'))
		self.assertEqual(404, r.status_code)

	@override_settings(ERROR_FILE=__file__)
	def test_errors_is_up(self):
		"""
		Check app returns with status 200
		"""

		r = self.c.get(reverse('kingdom.views.index.errors'))
		self.assertEqual(200, r.status_code)

	def test_dependencies_is_up(self):
		"""
		Check app returns with status 200
		"""

		r = self.c.get(reverse('kingdom.views.index.dependencies', args=('dot',)))
		self.assertEqual(200, r.status_code)

	def test_admin_is_up(self):
		"""
		Check admin returns with status 200
		"""

		r = self.c.get('/admin/')
		self.assertEqual(200, r.status_code)

	def test_admin_subpage_is_up(self):
		"""
		Check admin returns with status 200
		"""
		qc = QualityCategory(
			name="category"
		)
		qc.save()

		q = Quality(
			category = qc,
			slug="quality",
			name="quality"
		)
		q.save()

		r = self.c.get('/admin/kingdom/quality/1/')
		self.assertEqual(200, r.status_code)
