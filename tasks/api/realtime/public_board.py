from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .fetch_message import (
    get_board,
    save_board,
    SaveNotesWithUser,
    get_company_workplaces,
)


class BoardConsumer(AsyncWebsocketConsumer):

    online_users = {}

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

        message_type = data.get("type")

       
        if message_type == "join":

            self.username = data["username"]

            if self.room_name not in BoardConsumer.online_users:
                BoardConsumer.online_users[self.room_name] = set()

            BoardConsumer.online_users[self.room_name].add(
                self.username
            )

            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "presence_update",
                    "users": list(
                        BoardConsumer.online_users[self.room_name]
                    )
                }
            )

            return 

       
        if message_type == "board_update":

            username = data["username"]
            board_content = data["board_content"]

            await save_board(
                self.room_name,
                board_content
            )

            await SaveNotesWithUser(
                self.room_name,
                username,
                board_content
            )

        workplaces = await get_company_workplaces(self.room_name)

        for workplace in workplaces:

            await self.channel_layer.group_send(
                workplace.room_name,
                {
                    "type": "notification",
                    "username": username,
                    "message": f"updated {self.room_name}"
                }
            )

            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "board_update",
                    "board_content": board_content,
                }
            )

            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "notification",
                    "username": username,
                    "message": "updated the board",
                }
            )

            return
        
    async def notification(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "notification",
                "username": event["username"],
                "message": event["message"]
            })
        )

    async def board_update(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "board_update",
                "board_content": event["board_content"]
            })
        )

    async def presence_update(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "presence",
                "users": event["users"]
            })
        )

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

        if hasattr(self, "username"):

            BoardConsumer.online_users[self.room_name].discard(
                self.username
            )

            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "presence_update",
                    "users": list(
                        BoardConsumer.online_users[self.room_name]
                    )
                }
            )