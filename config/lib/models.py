import re

from datetime import datetime
from django.db import models, connection, transaction, IntegrityError
from django.db.models.loading import get_model
from django.core.exceptions import ValidationError


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


class ContextModel:
	"""
	An object with the ability to store some context in it.
	"""

	def get_value(self, name, default=None):
		"""
		Gets a value.
		Returns default if the value does not exists.
		"""
		kwargs = {
			'name': name,
			self.context_model: self
		}

		store = get_model(self.context_app, self.context_holder)

		try:
			v = store.objects.get(**kwargs)
		except store.DoesNotExist:
			return default

		return v.value

	def has_value(self, name):
		"""
		Returns True if this value exists on the object.
		"""

		kwargs = {
			'name': name,
			self.context_model: self
		}

		store = get_model(self.context_app, self.context_holder)

		try:
			v = store.objects.get(**kwargs)
			return True
		except store.DoesNotExist:
			return False

	def set_value(self, name, value):
		"""
		Sets a value
		"""

		if self.pk is None:
			raise ValidationError("Save before storing value.")

		kwargs = {
			self.context_model: self,
			'name': name,
			'value': value
		}

		# Run within a savepoint
		# Else, IntegrityError in Postgres are not recoverable.
		try:
			sid = transaction.savepoint()

			v = get_model(self.context_app, self.context_holder)(**kwargs)
			v.save()

			transaction.savepoint_commit(sid)
		except IntegrityError:
			transaction.savepoint_rollback(sid)

			# Now here is some weird behavior in
			# stored_value.py. Django does not seems to reexecute the get_prep_value code, so we can't overwrite an existing value with a new FK.
			# Therefore we need to delete it...
			del kwargs['value']
			v = get_model(self.context_app, self.context_holder).objects.get(**kwargs).delete()
			self.set_value(name, value)
	
	def get_values(self):
		kwargs = {
			self.context_model: self,
		}

		vs = get_model(self.context_app, self.context_holder).objects.filter(**kwargs)

		return {v.name: v.value for v in vs}


class ScriptedModel(models.Model):
	"""
	Model with the ability to run some code.
	"""

	class Meta:
		abstract = True

	"""
	Static variable.
	This one holds the stack for the current execution, to count direct and nested queries.

	Let's say we have a function f1 doing 2 direct queries and calling f2, doing 1 queries.
	Let's say the current number of queries is X.
	The final number of queries will be X + 2 + 1.
	Since all script code run within a ScriptedModel (see below), we can easily track the nested number of queries : juste store in the current context the total number of queries before launching the script, run the script, then compute number of queries - initial number of queries.

	It is not that easy to compute direct queries number, however this is the real metric we want to see.
	For that, we're simulating a computer stack with the variable below.
	Every script will add a new item at the end of the array with a value of 0.
	Every "child" will update his parents (__stack[-1]) to indicate how many queries must be substracted for being indirect.
	The initial caller will compute total number of queries minus indirect queries to get his own direct number.
	"""
	_stack = [0]

	"""
	Static variable.
	This one is holding all logs for the current stack.
	This will be saved once the outer-most item is reached, to avoid side-effect of counting INSERT INTO of the script logs itself.
	"""
	_scriptlogs = []

	def execute(self, model, attr, kingdom=None, raw_context=None):
		"""
		Execute the code stored in :attr on :model object, with :self as param. Context is built by default with :kingdom key, additional values can be passed with raw_context.
		"""

		from config.lib.execute import execute
		from reporting.models import ScriptLog

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
		ScriptedModel._stack.append(0)

		# Execute code
		code = getattr(model, attr)

		try:
			status, param = execute(code, self, context)
		except Exception as e:
			# Let's try to display something useful for the scripter team.
			import traceback
			import string

			# Retrieve the traceback.
			trace = traceback.format_exc().split("\n")

			print "@@@@@@@@@@@@@@@@@@@@@"
			print "@@ERROR in %s.%s(%s)" % (model.__class__.__name__, attr, model.pk)
			print "---------------------"
			print filter(lambda x: x in string.printable, code)
			print "@@@@@@@@@@@@@@@@@@@@@"

			raise

		# Retrieve metrics
		delay = (datetime.now() - _started_at).total_seconds() * 1000
		queries = len(connection.queries) - _started_query_count

		child_queries = ScriptedModel._stack.pop()
		direct_queries = queries - child_queries
		parent_nested_queries = ScriptedModel._stack[-1]
		ScriptedModel._stack[-1] = parent_nested_queries + queries

		# Store log
		if code is not None and code.strip() != "":
			sl = ScriptLog(
				kingdom=kingdom,
				object_type=model.__class__.__name__,
				object_pk=model.pk,
				object_attr=attr,
				stack_level=len(ScriptedModel._stack),
				time=delay,
				queries=queries,
				direct_queries=direct_queries
			)
			ScriptedModel._scriptlogs.append(sl)

		if len(ScriptedModel._stack) == 1:
			# We are at the root of a call-trace, let's save all script log
			ScriptLog.objects.bulk_create(ScriptedModel._scriptlogs)
			del ScriptedModel._scriptlogs[:]

		return status, param
