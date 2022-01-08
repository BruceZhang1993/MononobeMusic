import asyncio
import datetime
import math
from typing import Optional

import vlc

from mononobe_core.models import MononobeMedia, MononobeSong
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
            self.event_manager.event_attach(vlc.EventType.MediaPlayerMediaChanged, self.media_changed)
            self.event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.position_changed)

    def media_changed(self, _):
        media: vlc.Media = self.player.get_media()
        title = media.get_meta(vlc.Meta.Title)
        artist = media.get_meta(vlc.Meta.Artist)
        album = media.get_meta(vlc.Meta.Album)
        print(f'Playing\nTitle:   {title}\nArtists: {artist}\nAlbum:   {album}')

    def position_changed(self, _):
        duration = str(datetime.timedelta(seconds=math.floor(self.player.get_length() / 1000)))
        position = str(datetime.timedelta(seconds=math.floor(self.player.get_time() / 1000)))
        print(f'{position}/{duration}', end=" \r")

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

    async def async_play_song(self, song: MononobeSong):
        assert len(song.media) > 0
        media = self.instance.media_new(song.media[0].uri)
        media.set_meta(vlc.Meta.Title, song.name)
        media.set_meta(vlc.Meta.Artist, song.artists_name)
        media.set_meta(vlc.Meta.Album, song.album_name)
        self.player.set_media(media)
        self.player.play()
        self._playing = True
        while self._playing:
            await asyncio.sleep(1)

    async def async_play_uri(self, uri: str):
        media = self.instance.media_new(uri)
        self.player.set_media(media)
        self.player.play()
        self._playing = True
        while self._playing:
            await asyncio.sleep(1)
