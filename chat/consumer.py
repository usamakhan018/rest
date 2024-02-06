from .models import Chat, ChatMessage
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		print("ChatConsumer: connect")
		await self.accept()
	async def disconnect(self, code):
		print("ChatConsumer: disconnect")
		pass
	async def receive_json(self, content):
		print("ChatConsumer: receive_json")
		pass