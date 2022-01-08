import importlib
import pkgutil
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Optional

from mononobe_core.models import MononobeMedia, MononobeSong


class Player(metaclass=ABCMeta):
    @staticmethod
    def init(name: str = None) -> Optional['Player']:
        if name is None:
            # TODO: auto select by environment
            name = 'vlc'
        for _, modname, _ in pkgutil.iter_modules([Path(__file__).parent.as_posix()]):
            if modname == name + '_player':
                module = importlib.import_module('mononobe_core.player.' + modname)
                if hasattr(module, name.capitalize() + 'Player'):
                    return getattr(module, name.capitalize() + 'Player')()
        return None

    @abstractmethod
    def play_uri(self, uri: str):
        pass

    @abstractmethod
    async def async_play_uri(self, uri: str):
        pass

    @abstractmethod
    async def async_play_song(self, media: MononobeSong):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass


if __name__ == '__main__':
    Player.init('vlc').play_uri('http://music.163.com/song/media/outer/url?id=5238992.mp3')
