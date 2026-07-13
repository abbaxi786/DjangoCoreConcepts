from channels.db import database_sync_to_async
from ..models import Message,Board



@database_sync_to_async
def get_last_messages(room_name):
    messages = Message.objects.filter(
        room_name=room_name
    ).order_by("-created_at")[:20]

    return list(messages)


@database_sync_to_async
def save_message(room_name, username, message):
    Message.objects.create(
        room_name=room_name,
        username=username,
        message=message
    )
@database_sync_to_async
def save_board(room_name, board_content):
    board, created = Board.objects.get_or_create(
        room_name=room_name
    )

    board.board_content = board_content
    board.save()

    return board

@database_sync_to_async
def get_board(room_name):
    board, created = Board.objects.get_or_create(
        room_name=room_name
    )

    return board.board_content

