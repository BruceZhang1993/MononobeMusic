import importlib
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Optional, Union, Awaitable

from mononobe_core.enums import SearchType
from mononobe_core.models import MononobePagination, MononobeModel, MononobeSong, MononobeMedia
from mononobe_core.player import Player


class Provider(metaclass=ABCMeta):
    @staticmethod
    def init(name: str) -> Optional['Provider']:
        for directory in Path(__file__).parent.iterdir():
            directory: Path
            if directory.stem.startswith('_'):
                continue
            if directory.stem == name:
                module = importlib.import_module(f'mononobe_api.{name}')
                if hasattr(module, f'{name.capitalize()}Provider'):
                    return getattr(module, f'{name.capitalize()}Provider')()
        return None

    @abstractmethod
    def keyword_search(self, search_type: SearchType, keyword: str, page: int, page_size: int)\
            -> Union[MononobePagination[MononobeSong], Awaitable[MononobePagination[MononobeSong]]]:
        pass

    @abstractmethod
    def get_media(self, search_type: SearchType, identifier: str, bitrate: int) -> Optional[MononobeMedia]:
        pass


async def main():
    provider = Provider.init('local')
    songs = provider.keyword_search(SearchType.song, 'me', 1, 20)
    print(songs)
    return
    song: 'MononobeSong' = songs.data[0]
    player = Player.init('vlc')
    player.play_uri(song.media.uri)
    await asyncio.sleep(2)
    player.pause()
    await asyncio.sleep(2)
    player.resume()
    await asyncio.sleep(2)
    player.stop()


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
