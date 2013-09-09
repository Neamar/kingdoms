from internal.models import Function, Constant


def call_function(name, **kwargs):
	"""
	Call the function name with kwargs arguments
	"""

	f = Function.objects.get(slug=name)
	ret = f.fire(**kwargs)
	return ret


def c(name, **kwargs):
	"""
	Alias for call_function.
	"""

	return call_function(name, **kwargs)


def constant_value(name):
	return Constant.objects.get(name=name).value
Constant.v = staticmethod(constant_value)
