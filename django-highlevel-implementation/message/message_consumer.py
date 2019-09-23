# import json
#
from channels.generic.websocket import AsyncWebsocketConsumer


#
#
class MessageConsumer(AsyncWebsocketConsumer):
    """Consumer to manage WebSocket connections for the Message app,
    called when the websocket is handshaking as part of initial connection.
    """

    async def connect(self):
        pass

    async def disconnect(self, close_code):
        pass

    async def receive_text_message(self, text_message):
        pass

    async def receive_file_message(self, file_message):
        pass

    async def send_file_message_to_online_user(self, file_message):
        pass

    async def send_text_message_to_online_user(self, text_message):
        pass

    def add_text_message_to_database(self, text_message):
        pass

    def add_file_message_to_database(self, file_message):
        pass

    async def send_text_message_to_group_online_users(self, text_message):
        pass

    async def send_file_message_to_group_online_users(self, file_message):
        pass




