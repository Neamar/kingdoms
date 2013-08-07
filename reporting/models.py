from django.db import models
from kingdom.models import Kingdom


class ScriptLog(models.Model):
	"""
	Store execution time for each code.
	"""

	kingdom = models.ForeignKey(Kingdom, null=True, default=None, on_delete=models.SET_NULL)

	object_type = models.CharField(max_length=100)
	object_pk = models.PositiveIntegerField()
	object_attr = models.CharField(max_length=100)

	stack_level = models.PositiveIntegerField(help_text="Number of calls before this one in the stack.")
	time = models.PositiveIntegerField(help_text="Time to run, in milliseconds.")
	direct_queries = models.PositiveIntegerField(help_text="Number of direct queries or None.", default=None, null=True)
	queries = models.PositiveIntegerField(help_text="Total number of queries, including stack or None.", default=None, null=True)

	def __unicode__(self):
		return "%s(%s).%s" % (self.object_type, self.object_pk, self.object_attr)

