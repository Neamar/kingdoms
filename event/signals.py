# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.conf import settings
from django.template import Template, Context
from django.utils.functional import memoize

from kingdom.management.commands.cron import cron_minute, cron_ten_minutes
from event.models import PendingEvent, PendingEventAction, EventCategory, PendingEventToken

from random import randint

@receiver(post_save, sender=PendingEvent)
def set_event_actions_and_fire(sender, instance, created, **kwargs):
	"""
	Create all pending event actions from event actions on start.
	"""

	if instance.started and instance.started <= datetime.now() and not instance.is_started:
		# Only fire and create actions after started is set.

		# Check condition
		status = instance.check_condition()
		if status != 'ok':
			instance.delete()
			raise ValidationError("Impossible de créer cet évènement : %s" % status)

		status, param = instance.fire()

		if status != 'ok':
			# The event asks not to be displayed.
			instance.delete()
			return

		from django.template import add_to_builtins
		add_to_builtins("kingdom.templatetags.folks_list")
		add_to_builtins("kingdom.templatetags.feminize")
		add_to_builtins("kingdom.templatetags.number")
		add_to_builtins("kingdom.templatetags.elide")
		add_to_builtins("kingdom.templatetags.folk_details")

		raw_context = {}
		raw_context['kingdom'] = instance.kingdom
		raw_context['folks'] = instance.kingdom.folk_set.all()
		raw_context['dynasty'] = lambda: instance.kingdom.user.username

		# Access to folk in titles using title.[title_name]
		titles = lambda: {at.title.slug: at.folk for at in instance.kingdom.availabletitle_set.all().select_related('title')}
		raw_context['title'] = memoize(titles, {}, 0)

		# Access to kingdom values using kingdom.values.[name]
		raw_context['kingdom'].values = memoize(instance.kingdom.get_values, {}, 0)

		raw_context.update(instance.get_values())

		context = Context(raw_context, autoescape=False)

		try:
			settings.TEMPLATE_STRING_IF_INVALID = "<tt style='color:red'>{{%s}}</tt>"

			# Create text from templates
			text_template = Template(instance.event.text)
			instance.text = text_template.render(context)

			instance.is_started = True
			instance.save()

			for event_action in instance.event.eventaction_set.all():
				text_template = Template(event_action.text)
				message_template = Template(event_action.message)
				pea = PendingEventAction(
					pending_event=instance,
					event_action=event_action,
					text=text_template.render(context),
					message=message_template.render(context),
				)

				status = pea.check_condition()
				if status == 'ok':
					pea.save()
		except:
			raise
		finally:
			settings.TEMPLATE_STRING_IF_INVALID = ''

@receiver(pre_save, sender=PendingEventAction)
def check_pending_event_action_sanity(sender, instance, **kwargs):
	"""
	Check the actions refers to this event.
	"""

	if instance.event_action.event != instance.pending_event.event:
		raise IntegrityError("The events in EventAction and PendingEventAction are different ")


@receiver(cron_minute)
def cron_start_future_pendingevent(sender, counter, **kwargs):
	"""
	"Wake" pending_event registered for the future when their times has come.
	"""

	pending_events = PendingEvent.objects.filter(is_started=False, started__lte=datetime.now())

	for pending_event in pending_events:
		# Will trigger the post-save signal set_event_actions_and_fire
		try:
			pending_event.save()
		except ValidationError:
			# The pending event asked not to be displayed and has been deleted.
			pass

@receiver(cron_ten_minutes)
def cron_token_dealer(sender, counter, **kwargs):
	"""
	Create pending_event_token
	"""
	tokens = []
	for cat in EventCategory.objects.all():
		for kingdom in cat.available_kingdoms.all():
			if randint(1, cat.frequency) == cat.frequency:
				pending_event_token = PendingEventToken(
					kingdom=kingdom,
					category = cat
				)
				tokens.append(pending_event_token)

	# Bulk create in a single query
	PendingEventToken.objects.bulk_create(tokens)

