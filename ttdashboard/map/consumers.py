import json
from channels import layers
from channels.generic.websocket import AsyncWebsocketConsumer

from .serializers import GameSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_sf']
        self.room_group_name = f'game_{self.room_name}'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def shoot(self, event):
        await self.send(text_data=json.dumps({
            'event': 'shoot',
            'data': event['data'],
            'new_game_data': event["new_game_data"]
        }))

    async def move(self, event):        
        await self.send(text_data=json.dumps({
            'event': 'move',
            'data': event['data'],
            'new_game_data': event["new_game_data"]
        }))

    async def upgrade(self, event):        
        await self.send(text_data=json.dumps({
            'event': 'upgrade',
            'data': event['data'],
            'new_game_data': event["new_game_data"]
        }))

    async def transfer(self, event):        
        await self.send(text_data=json.dumps({
            'event': 'transfer',
            'data': event['data'],
            'new_game_data': event["new_game_data"]
        }))

    async def vote(self, event):        
        await self.send(text_data=json.dumps({
            'event': 'vote',
            'data': event['data'],
            'new_game_data': event["new_game_data"]
        }))
    
    async def new_ad(self, event):
        print(event)
        await self.send(text_data=json.dumps({
            'event': 'new_ad',
            "data": event["data"],
            'new_game_data': event["new_game_data"]
        }))
