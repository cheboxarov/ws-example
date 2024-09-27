from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
import asyncio
from .models import GraphLog
from asgiref.sync import sync_to_async


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

    async def connect(self):
        await self.accept()
        for i in range(1000):
            edits = await sync_to_async(GraphLog.objects.count)()
            data = {
                "edits": edits,
                "value": randint(1, 100),
                "day": next(self.days_generator)
            }

            await self.send(json.dumps(data))
            print(data.pop("edits"))
            await sync_to_async(GraphLog.objects.create)(**data)
            await asyncio.sleep(1)
