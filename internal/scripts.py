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


def C(name):
	"""
	Quick access to constant values
	"""

	return Constant.objects.get(name=name).value


def S(name):
	"""
	Quick access to status values
	"""

	return Status.objects.get(name=name).value


def constant_value(name):
	return Constant.objects.get(name=name).value
Constant.v = staticmethod(constant_value)
