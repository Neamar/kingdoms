# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError

from kingdom.models import Kingdom, Folk


class StoredValueTest(TestCase):
	"""
	Unit tests for stored values
	"""
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
		)
		self.f.save()

	def test_kingdom_value_store_string(self):
		"""
		Store string values on the kingdom
		"""

		self.k.set_value("foo", "bar")

		self.assertEqual(self.k.get_value("foo"), "bar")

	def test_kingdom_value_store_int(self):
		"""
		Store int values on the kingdom
		"""

		self.k.set_value("foo", 2)

		self.assertEqual(self.k.get_value("foo"), 2)

	def test_kingdom_value_store_float(self):
		"""
		Store float values on the kingdom
		"""

		self.k.set_value("foo",  1.25)

		self.assertEqual(self.k.get_value("foo"),  1.25)

	def test_kingdom_value_store_boolean(self):
		"""
		Store int values on the kingdom
		"""

		self.k.set_value("foo", True)
		self.k.set_value("foo2", False)

		self.assertEqual(self.k.get_value("foo"), True)
		self.assertEqual(self.k.get_value("foo2"), False)

	def test_kingdom_value_store_fk(self):
		"""
		Store foreign keys values on the kingdom
		"""

		self.k.set_value("foo", self.f)

		self.assertEqual(self.k.get_value("foo"), self.f)

	def test_kingdom_value_store_fk_unsaved(self):
		"""
		Can't store unsaved models.
		"""

		f2 = Folk(kingdom=self.k)

		self.assertRaises(ValidationError, (lambda: self.k.set_value("foo", f2)))

	def test_kingdom_value_store_fk_deletion(self):
		"""
		Deleted values yields None
		"""

		self.k.set_value("foo", self.f)

		self.f.delete()
		self.assertEqual(self.k.get_value("foo"), None)

	def test_kingdom_value_store_empty_list(self):
		"""
		Store empty array values on the kingdom
		"""

		datas = []
		self.k.set_value("foo", datas)

		self.assertEqual(self.k.get_value("foo"), datas)

	def test_kingdom_value_store_mixed_list(self):
		"""
		Store array values on the kingdom
		"""

		datas = [1, 2, "lol", True]
		self.k.set_value("foo", datas)

		self.assertEqual(self.k.get_value("foo"), datas)

	def test_kingdom_value_store_nested_list(self):
		"""
		Store nested array values on the kingdom
		"""

		datas = [[self.f, 1, 2], [self.k, 1, 2]]
		self.k.set_value("foo", datas)

		self.assertEqual(self.k.get_value("foo"), datas)

	def test_kingdom_value_store_nested_dict(self):
		"""
		Store nested dict values on the kingdom
		"""

		datas = {
			'man': "himself",
			'woman': {
				"lol": "herself"
			}
		}

		self.k.set_value("foo", datas)

		self.assertEqual(self.k.get_value("foo"), datas)

	def test_kingdom_value_store_queryset_fk(self):
		"""
		Store queryset values on the kingdom
		"""

		Folk(kingdom=self.k).save()
		Folk(kingdom=self.k).save()
		Folk(kingdom=self.k).save()
		datas = Folk.objects.all()
		self.k.set_value("foo", datas)

		real_folks = Folk.objects.all()
		stored_folks = self.k.get_value("foo")
		for r, s in zip(real_folks, stored_folks):
			self.assertEqual(r, s)

	def test_kingdom_value_store_list_fk(self):
		"""
		Store list of fk values on the kingdom
		"""

		f2 = Folk(kingdom=self.k)
		f2.save()
		datas = [self.f, f2, True, 0, "trololol"]
		self.k.set_value("foo", datas)

		stored_datas = self.k.get_value("foo")
		for r, s in zip(datas, stored_datas):
			self.assertEqual(r, s)

	def test_kingdom_value_store_mixin(self):
		"""
		Mixin values.
		"""

		datas = {
			'string': "string",
			'array': [1, 2, 3],
			'fk': self.k,
			'none': None,
			'bool': True,
			'mixed_array': [1, None, self.f],
			'nested_arrays': [1, 2, [3, 4, [5, 6]]],
			'nested_object': {
				'outofidea': True
			}
		}

		self.k.set_value("foo", datas)

		self.assertEqual(self.k.get_value("foo"), datas)

	def test_kingdom_value_retrieve_undefined(self):
		"""
		Non existing values returns default value, or None
		"""

		self.assertEqual(self.k.get_value("foo"), None)
		self.assertEqual(self.k.get_value("foo", "bar"), "bar")

	def test_kingdom_value_retrieve_all(self):
		"""
		get_values retrieve all values.
		"""

		obj = {
			'val1': 1,
			'val2': "Hello",
			'val3': True,
			'val4': self.k
		}

		for k, v in obj.items():
			self.k.set_value(k, v)

		self.assertEqual(self.k.get_values(), obj)

	def test_kingdom_has_value(self):
		"""
		Test has_value code
		"""

		self.assertFalse(self.k.has_value("foo"))

		self.k.set_value('foo', 'bar')

		self.assertTrue(self.k.has_value("foo"))

	def test_kingdom_value_overwrite(self):
		"""
		Test we can write to the same value multiple time.
		"""

		self.k.set_value('foo', 'bar')
		self.assertEqual(self.k.get_value("foo"), 'bar')

		self.k.set_value('foo', 223)
		self.assertEqual(self.k.get_value("foo"), 223)

		self.k.set_value('foo', self.k)
		self.assertEqual(self.k.get_value("foo"), self.k)

		self.k.set_value('foo', self.f)
		self.assertEqual(self.k.get_value("foo"), self.f)
