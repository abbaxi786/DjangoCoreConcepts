from django.urls import path
from .realtime.consumer import ChatConsumer
from .realtime.public_board import BoardConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
    path("ws/board/<str:room_name>/", BoardConsumer.as_asgi()),
]