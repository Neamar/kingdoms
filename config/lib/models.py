from datetime import datetime
from django.db import models
from django.db import connection


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


__stack = []


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
		from internal.models import ScriptLog

		# Build context object
		context = {}
		if kingdom is not None:
			context = {
				'kingdom': kingdom,
				'folks': kingdom.folk_set.all(),
			}

		if raw_context is not None:
			context.update(raw_context)

		_started_at = datetime.now()
		_started_query_count = len(connection.queries)
		__stack.append(_started_query_count)
		# Execute code
		code = getattr(model, attr)
		status, param = execute(code, self, context)

		delay = (datetime.now() - _started_at).total_seconds() * 1000
		nested_queries = len(connection.queries) - _started_query_count
		queries = len(connection.queries) - _started_query_count

		# Store log
		if code is not None and code != "":
			ScriptLog(
				kingdom=kingdom,
				object_type=model.__class__.__name__,
				object_pk=model.pk,
				object_attr=attr,
				time=delay,
				nested_queries=nested_queries,
				queries=queries
			).save()

		return status, param
