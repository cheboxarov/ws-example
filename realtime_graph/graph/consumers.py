from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
import asyncio
from .models import GraphLog
from asgiref.sync import sync_to_async
from .serializers import GraphLogSerializer
from channels.db import database_sync_to_async


def get_day():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    index = 0
    while True:
        yield days[index]
        index += 1
        if index == 6:
            index = 0




class GraphConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.days_generator = get_day()
        super().__init__(*args, **kwargs)

    @database_sync_to_async
    def get_session_seed(self):
        return self.scope["session"].get("seed")
    
    @database_sync_to_async
    def set_session_seed(self, seed: int):
        self.scope["session"]["seed"] = seed
        self.scope["session"].save()

    async def connect(self):
        seed = await self.get_session_seed()
        print(seed)
        if not seed:
            await self.set_session_seed(randint(1, 1000))
        await self.accept()
        for i in range(1000):
            logs = await sync_to_async(list)(GraphLog.objects.order_by("-id")[:100])
            serializer = GraphLogSerializer(logs, many=True)
            serialized_data = serializer.data
            edits = await sync_to_async(GraphLog.objects.count)()

            data = {
                "edits": edits,
                "value": randint(1, 100),
                "day": next(self.days_generator),
                "logs": serialized_data
            }

            await self.send(json.dumps(data))

            data.pop("edits")
            await sync_to_async(GraphLog.objects.create)(**{
                "value": data.get("value"),
                "day": data.get("day")
            })

            await asyncio.sleep(1)
