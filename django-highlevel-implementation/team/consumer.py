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

    async def add_member_to_team(self, team_id, adder_info, member_info):
        pass

    async def notify_member_added_to_team(self, group_id, adder_info, member_info):
        pass

    async def make_coleader_in_team(self, memnber_info, team_id):
        pass

    async def notify_memeber_became_coleader_of_team(self, team_id, info):
        pass

    async def notify_memebers_project_creation(self, team_id, project_info, creator):
        pass

    async def notify_memebers_task_creation(self, team_id, task_info, creator):
        pass

    async def notify_memebers_task_memeber_addition(self, team_id, project_id, task_info, member_info, assigner):
        pass

    async def notify_memebers_task_result_upload(self, team_id, project_id, task_info, member_updated, result):
        pass

    async def team_settings_changed(self, team_id, new_settings):
        pass

    async def project_settings_changed(self, project_id, new_settings):
        pass

    async def task_settings_changed(self, task_id, new_settings):
        pass
