
from discordrp import Presence
class DiscordRpc:
    def __init__(self, client):
        self.client = client
        self.presence = Presence(client)
    def set(self, info):
        self.presence.set(info)
    def pause(self):
        self.presence.clear()
