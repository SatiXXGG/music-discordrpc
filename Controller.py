from Presence import DiscordRpc
from Music import AppleMusicWrapper
from time import sleep as s
from time import time
from math import floor
class Controller:
    def __init__(self, client):
        self.Presence = DiscordRpc(client)
        self.Music = AppleMusicWrapper()
        self.isPaused = True
        self.lastPaused = time()

    def update(self):
        try:
            if not self.Music.appleMusicIsOpen():
                print("Apple music is not opened")
                print("This only works with songs on your library!")
                self.Presence.clear()
                return

            position = floor(float(self.Music.getSongPosition()))
            length = floor(float(self.Music.getTrackLength()))
            current = int(time())
            start = current - position
            end = start + length

            state = self.Music.getSongState().strip()

            if (state == "paused" and self.isPaused == False):
                self.lastPaused = current
                self.isPaused = True
            elif (state == "playing" and self.isPaused == True):
                self.isPaused = False

            timeSincePause = current - self.lastPaused
            if (timeSincePause > 15 and self.isPaused == True):
                print("presence has been cleared")
                self.Presence.pause()
                return

            if (state == "paused"):
                self.Presence.set({
                    "name": self.Music.getArtist(),
                    "type": 2,
                    "details": self.Music.getSong(),
                    "state": f"Paused - {self.Music.getTrackAlbum()}",
                    "assets": {
                        "large_image": self.Music.getAlbumCover(),
                    },
                })
            elif state == "playing":
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

        except:
            print("Error updating presence safely ignore if you're not using a music player")

    def start(self):
        try:
            while True:
                self.update()
                s(1)

        except:
            pass
