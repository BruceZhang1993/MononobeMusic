import asyncio
from typing import Optional

import vlc

from mononobe_core.player import Player


class VlcPlayer(Player):
    def __init__(self):
        self._playing = False
        self.instance: Optional[vlc.Instance] = vlc.Instance()
        self.player: vlc.MediaPlayer = self.instance.media_player_new() if self.instance is not None else None
        self.event_manager: Optional[vlc.EventManager] = None
        if self.player:
            self.event_manager = self.player.event_manager()
            self.event_manager.event_attach(vlc.EventType.MediaPlayerStopped, self.stopped)

    def stopped(self, _):
        self._playing = False

    def stop(self):
        self._playing = False
        self.player.stop()

    def pause(self):
        self.player.pause()

    def resume(self):
        self.player.play()

    def play_uri(self, uri: str):
        media = self.instance.media_new(uri)
        self.player.set_media(media)
        self.player.play()

    async def async_play_uri(self, uri: str):
        media = self.instance.media_new(uri)
        self.player.set_media(media)
        self.player.play()
        self._playing = True

        while self._playing:
            await asyncio.sleep(1)
