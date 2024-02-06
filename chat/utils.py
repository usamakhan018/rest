from .models import Chat

def get_or_create_chat(user1, user2):
	try:
		chat = Chat.objects.get(user1=user1, user2=user2)
	except Chat.DoesNotExist:
		try:
			chat = Chat.objects.get(user2=user2, user1=user1)
		except Chat.DoesNotExist:
			chat = Chat.objects.create(user1=user1, user2=user2)
	return chat