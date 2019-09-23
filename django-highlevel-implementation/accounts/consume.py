# import json
#
from channels.generic.websocket import AsyncWebsocketConsumer


#
#
class Consumer(AsyncWebsocketConsumer):

    async def connect(self):
        pass

    async def disconnect(self, close_code):
        pass

    async def update_profile(self, info):
        pass
