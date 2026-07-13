from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .fetch_message import get_board, save_board


class BoardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

        board_content = await get_board(self.room_name)

        await self.send(
            text_data=json.dumps({
                "type": "initial_board",
                "board_content": board_content
            })
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        board_content = data["board_content"]

        await save_board(
            self.room_name,
            board_content
        )

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "board_update",
                "board_content": board_content
            }
        )

    async def board_update(self, event):
        await self.send(
            text_data=json.dumps({
                "type": "board_update",
                "board_content": event["board_content"]
            })
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )