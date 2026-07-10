from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        await self.send(text_data=json.dumps({
            "message": "Connected!"
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.send(text_data=json.dumps({
            "username": data["username"],
            "message": data["message"]
        }))

    async def disconnect(self, close_code):
        print("Disconnected")