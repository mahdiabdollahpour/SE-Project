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

    async def add_member_to_group(self, group_id, adder_info, member_info):
        pass

    async def notify_online_users_of_group(self, group_id, info):
        pass

    # except user added
    # async def notify_online_users_of_group(self, group_id, adder_info, member_info):
    #     pass

    async def notify_memeber_added_to_group(self, group_id, info):
        pass

    # except user added
    async def make_coleader_in_group(self, memnber_info, group_id):
        pass

    async def notify_memeber_became_coleader_of_group(self, group_id, info):
        pass

    async def group_settings_changed(self, group_id, new_settings):
        pass
