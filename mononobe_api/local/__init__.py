import base64
from mimetypes import guess_type
from pathlib import Path
from typing import Union, Awaitable, List, Tuple, Optional
import mutagen

from mononobe_api import Provider
from mononobe_core.enums import SearchType
from mononobe_core.exceptions import MononobeNotImplemented
from mononobe_core.models import MononobePagination, MononobeModel, MononobeSong, MononobeMedia

LOCAL_MUSIC_DIR = Path.home() / 'Music'


class LocalProvider(Provider):

    def show_media(self, media_type: SearchType, identifier: str) -> Optional[MononobeSong]:
        pass

    def __init__(self):
        self._songs: List[MononobeSong] = []
        self.load_library()

    @staticmethod
    def is_music(file: Path):
        if not file.is_file():
            return False
        mime, _ = guess_type(file)
        return mime is not None and mime.startswith('audio')

    def load_library(self):
        for f in LOCAL_MUSIC_DIR.glob('**/*'):
            if not self.is_music(f):
                continue
            title, artist, album, duration = self.load_metadata(f)
            artist_model = MononobeSong.Artist(id=base64.b64encode(artist.encode()).decode(), name=artist, provider='local')
            album_model = MononobeSong.Album(id=base64.b64encode(album.encode()).decode(), name=album, provider='local')
            self._songs.append(MononobeSong(id=base64.b64encode(f.as_posix().encode()).decode(), provider='local',
                                            name=title, duration=duration, media=MononobeMedia(uri=f.as_posix()),
                                            artists=[artist_model], album=album_model))

    @staticmethod
    def load_metadata(f: Path) -> Tuple[str, str, str, int]:
        mime, _ = guess_type(f)
        file = mutagen.File(f)
        title = ''
        artist = ''
        album = ''

        if mime.endswith('mpeg'):
            title = str(file['TIT2'])
            artist = str(file['TPE1'])
            album = str(file['TALB'])
        elif mime.endswith('flac'):
            title = str(file['title'][0])
            artist = str(file['artist'][0])
            album = str(file['album'][0])

        return title, artist, album, file.info.length

    @staticmethod
    def filter_song_by_name(song: MononobeSong, keyword: str) -> bool:
        return song.name.lower().find(keyword.lower()) != -1

    def keyword_search(self, search_type: SearchType, keyword: str, page: int, page_size: int)\
            -> Union[MononobePagination[MononobeModel], Awaitable[MononobePagination[MononobeModel]]]:
        data = list(filter(lambda s: self.filter_song_by_name(s, keyword), self._songs))
        return MononobePagination(page=page, page_size=page_size, total=len(data), data=data[page_size * (page - 1):page_size])

    def get_media(self, search_type: SearchType, identifier: str, bitrate: int = None) -> Optional[MononobeMedia]:
        if search_type == SearchType.song:
            return MononobeMedia(uri=base64.b64decode(identifier).decode())
        raise MononobeNotImplemented()


if __name__ == '__main__':
    LocalProvider()
