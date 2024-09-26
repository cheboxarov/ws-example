from channels.generic.websocket import WebsocketConsumer
import json
from random import randint
from time import sleep


class WSConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        for i in range(1000):
            message = {
                "message": randint(1, 100)
            }
            data = json.dumps(message)
            self.send(data)
            sleep(1)

