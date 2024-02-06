from django.db import models
from django.conf import settings

class Chat(models.Model):
	user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chat_user1", on_delete=models.CASCADE)
	user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chat_user2", on_delete=models.CASCADE)
	connected_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chat_connected_users", blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f"chat between {self.user1} and {self.user2}"

	def connect_user(self, user):
		connected = False
		if not user in self.connected_users.all():
			self.connected_users.add(user)
			connected = True
		return connected

	def disconnect_user(self, user):
		disconnected = False
		if user in self.connected_users.all():
			self.connected_users.remove(user)
			disconnected = True
		return disconnected

	@property
	def group_name(self):
		return f"Chat-{self.pk}"



class ChatMessage(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chat_messages", on_delete=models.CASCADE)
	chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
	message = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} messaged {self.message}"
		