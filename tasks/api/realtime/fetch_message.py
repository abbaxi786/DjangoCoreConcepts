from channels.db import database_sync_to_async
from ..models import Message,Board,Note,WorkPlace



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

@database_sync_to_async
def SaveNotesWithUser(room_name, username, content):
    workplace = WorkPlace.objects.get(room_name=room_name)

    note = Note.objects.create(
        work_place=workplace,
        username=username,
        content=content
    )

    return note

@database_sync_to_async
def get_company_workplaces(room_name):

    workplace = WorkPlace.objects.select_related(
        "project__company"
    ).get(room_name=room_name)

    company = workplace.project.company

    return list(
        WorkPlace.objects.filter(
            project__company=company
        ).exclude(
            room_name=room_name
        )
    )
        

