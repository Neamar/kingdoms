from django.dispatch import Signal
from django.core.exceptions import ValidationError

class DisableSignals():
	"""
	Disable all signals from the app.
	Use with care, for very special cases.
	"""
	def __enter__(self):
		if hasattr(Signal, 'is_rigged'):
			raise ValidationError("Don't nest DisableSignals()!")

		Signal.send_original = Signal.send
		Signal.is_rigged=True
		def monkeypatch_send(self, sender, **named):
			return []
		Signal.send = monkeypatch_send

	def __exit__(self, type, value, traceback):
		Signal.send = Signal.send_original
		del Signal.send_original
		del Signal.is_rigged
