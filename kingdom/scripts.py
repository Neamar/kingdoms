from kingdom.models import Message, Kingdom


def kingdom_message(self, content):
	Message(
		kingdom=self,
		content=content
	).save()
Kingdom.message = kingdom_message
