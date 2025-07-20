from Presence import DiscordRpc
from Music import AppleMusicWrapper
from time import sleep as s
from time import time
from math import floor
class Controller:
    def __init__(self, client):
        self.Presence = DiscordRpc(client)
        self.Music = AppleMusicWrapper()
        self.lastSong = ""

    def update(self):
        if not self.Music.appleMusicIsOpen():
            print("Apple music is not opened")
            print("This only works with songs on your library!")
            self.Presence.clear()
            return


        try:
            position = floor(float(self.Music.getSongPosition()))
            length = floor(float(self.Music.getTrackLength()))
            current = int(time())
            start = current - position
            end = start + length



            self.Presence.set({
                "name": self.Music.getArtist(),
                "type": 2,
                "details": self.Music.getSong(),
                "state": self.Music.getTrackAlbum(),
                "assets": {
                    "large_image": self.Music.getAlbumCover(),
                },
                "timestamps": {
                    "start": start,
                    "end": end
                },
            })

            self.lastSong = self.Music.getSong()
        except:
            print("Error updating presence safely ignore if you're not using a music player")

    def start(self):
        try:
            while True:
                if (self.lastSong != self.Music.getSong()):
                    self.update()
                    s(1)
                else:
                    self.update()
                    s(5)
        except:
            pass
