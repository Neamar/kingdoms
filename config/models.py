from django.db import models


class NamedModel(models.Model):
	class Meta:
		abstract = True

	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name


class DescribedModel(NamedModel):
	class Meta:
		abstract = True

	description = models.TextField()
