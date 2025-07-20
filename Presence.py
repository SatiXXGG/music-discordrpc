
from discordrp import Presence
from time import sleep as s
from time import time
class DiscordRpc:
    def __init__(self, client):
        self.client = client
        self.presence = Presence(client)

    def _update(self):
        self.presence.update()
    def set(self, info):
        self.presence.set(info)
    def clear(self):
        self.presence.clear()
