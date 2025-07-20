
import subprocess as sp
import requests

class AppleMusicWrapper:
    def __init__(self):
        self.appName = "Music"
        pass
    def getTrackAlbum(self):
        try:
            return sp.check_output(['osascript', '-e', f'tell application "{self.appName}" to get album of current track']).decode('utf-8')
        except:
            return None
    def getSongState(self):
        try:
            return sp.check_output(['osascript', '-e', f'tell application "{self.appName}" to get player state']).decode('utf-8')
        except:
            return None
    def getTrackLength(self):
        try:
            return sp.check_output(['osascript', '-e', f'tell application "{self.appName}" to get duration of current track']).decode('utf-8')
        except:
            return 60
    def getSong(self):
        try:
            return sp.check_output(['osascript', '-e', f'tell application "Music" to get name of current track']).decode('utf-8')
        except:
            return "Error getting the song"
    def getImage(self):
        try:
            return sp.check_output(['osascript', '-e', f'tell application "{self.appName}" to get album art of current track']).decode('utf-8')
        except:
            return None
    def getArtist(self):
        try:
            return sp.check_output(['osascript', '-e', f'tell application "{self.appName}" to get artist of current track']).decode('utf-8')
        except:
            return None
    def getSongPosition(self):
        try:
            return sp.check_output(['osascript', '-e', f'tell application "{self.appName}" to get player position']).decode('utf-8')
        except:
            return 0
    def getInfo(self):
        return {
            "album": self.getTrackAlbum(),
            "song": self.getSong(),
            "art": self.getImage(),
            "artist": self.getArtist()
        }
    def getAlbumCover(self):
        query = f"{self.getSong()} {self.getArtist()}"
        url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
        r = requests.get(url)
        if r.status_code == 200:
            results = r.json().get("results")
            if results:
                return results[0]["artworkUrl100"].replace("100x100bb", "512x512bb")
        return None
    def isPlaying(self):
        return self.getSongState() == "Playing"
    def appleMusicIsOpen(self):
        try:
            result = sp.check_output([
                'osascript',
                '-e', f'tell application "System Events" to (name of processes) contains "{self.appName}"'
            ])
            return result.strip().decode('utf-8') == 'true'
        except:
            return False
    def init():
        pass
