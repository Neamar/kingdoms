from django.db import models


class NamedModel(models.Model):
	"""
	Model with a unique name.
	"""

	class Meta:
		abstract = True

	name = models.CharField(max_length=255, unique=True)

	def __unicode__(self):
		return self.name


class DescribedModel(NamedModel):
	"""
	Model with unique name and description.
	"""

	class Meta:
		abstract = True

	description = models.TextField()


class ScriptedModel(models.Model):
	"""
	Model with the ability to run some code.
	"""
	class Meta:
		abstract = True

	def execute(self, model, attr, kingdom, raw_context=None):
		"""
		Execute the code stored in :attr on :model object, with :self as param. Context is built by default with :kingdom key, additional values can be passed with raw_context.
		"""

		from config.lib.execute import execute

		# Build context object
		context = {}
		if kingdom is not None:
			context = {
				'kingdom': kingdom,
				'folks': kingdom.folk_set.all(),
			}

		if raw_context is not None:
			context.update(raw_context)

		# Execute code
		status, param = execute(getattr(model, attr), self, context)

		return status, param
