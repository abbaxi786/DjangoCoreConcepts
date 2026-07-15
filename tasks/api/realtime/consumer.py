
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .fetch_message import get_last_messages,save_message
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes

# @permission_classes([IsAuthenticated])
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("1. connect() called")

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        await self.channel_layer.group_add(
        self.room_name,
        self.channel_name
        )

        print("3. Group added")

        await self.accept()
        messages = await get_last_messages(self.room_name)
        messages.reverse()

        for msg in messages:
            await self.send(text_data=json.dumps({
                "type": "history",
                "username": msg.username,
                "message": msg.message,
                "created_at": str(msg.created_at)
            }))

        print("4. Connection accepted")

    async def receive(self, text_data):
        data = json.loads(text_data)

        username = data["username"]
        message = data["message"]

        await save_message(
            self.room_name,
            username,
            message
        )

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "username": username,
                "message": message
            }
        )
    async def chat_message(self, event):
        print("8. Sending to client")

        await self.send(
            text_data=json.dumps({
                "username": event["username"],
                "message": event["message"],
            })
        
        )

    async def disconnect(self, close_code):
        print("9. Disconnect:", close_code)

        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )