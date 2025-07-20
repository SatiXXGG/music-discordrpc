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
        self.lastSong = ""
        self.cachedImage = ""
        self.cachedAlbum = ""
        self.cachedArtist = ""

    def update(self):
        try:
            if not self.Music.appleMusicIsOpen():
                self.Presence.clear()
                print("cleared presence")
                return

            currentSong = self.Music.getSong()

            if (currentSong != self.lastSong):
                self.cachedImage = self.Music.getImage()
                self.cachedAlbum = self.Music.getTrackAlbum()
                self.cachedArtist = self.Music.getArtist()

            position = floor(float(self.Music.getSongPosition()))
            length = floor(float(self.Music.getTrackLength()))
            current = int(time())
            start = current - position
            end = start + length
            state = self.Music.getSongState().strip()
            timeSincePause = current - self.lastPaused

            if (state == "paused" and self.isPaused == False):
                self.lastPaused = current
                self.isPaused = True
            elif (state == "playing" and self.isPaused == True):
                self.isPaused = False

            if (timeSincePause > 15 and self.isPaused == True):
                self.Presence.pause()
                return

            if (state == "paused"):
                self.Presence.set({
                    "name": self.cachedArtist,
                    "type": 2,
                    "details": currentSong,
                    "state": f"Paused - {self.cachedAlbum}",
                    "assets": {
                        "large_image": self.cachedImage,
                    },
                })
            elif state == "playing":
                self.Presence.set({
                    "name": self.cachedArtist,
                    "type": 2,
                    "details": currentSong,
                    "state": self.cachedAlbum,
                    "assets": {
                        "large_image": self.cachedImage,
                    },
                    "timestamps": {
                        "start": start,
                        "end": end
                    },
                })

            self.lastSong = currentSong
        except:
            self.Presence.pause()
            print("Error updating presence safely ignore if you're not using a music player")

    def start(self):
        try:
            while True:
                self.update()
                s(8)

        except:
            pass
