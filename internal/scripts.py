from internal.models import Function, Constant, Status


def call_function(name, **kwargs):
	"""
	Call the function name with kwargs arguments
	"""

	f = Function.objects.get(slug=name)
	ret = f.fire(**kwargs)
	return ret


def f(name, **kwargs):
	"""
	Alias for call_function.
	"""

	return call_function(name, **kwargs)


class _MagicWrapper(type):
	def __getattr__(cls, name):
		return cls.get(name)
		
class C:
	"""
	Quick access to constant values
	"""
	__metaclass__ = _MagicWrapper

	@staticmethod
	def get(name):
		return Constant.objects.get(name=name).value


class S:
	"""
	Quick access to status values
	"""
	__metaclass__ = _MagicWrapper

	@staticmethod
	def get(name):
		return Status.objects.get(name=name).value


def constant_value(name):
	return Constant.objects.get(name=name).value
Constant.v = staticmethod(constant_value)
