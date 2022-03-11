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

    def _get_model_from_file(self, f: Path) -> MononobeSong:
        title, artist, album, duration, bitrate = self.load_metadata(f)
        artist_model = MononobeSong.Artist(id=base64.b64encode(artist.encode()).decode(), name=artist,
                                           provider='local')
        album_model = MononobeSong.Album(id=base64.b64encode(album.encode()).decode(), name=album, provider='local')
        return MononobeSong(id=base64.b64encode(f.as_posix().encode()).decode(), provider='local',
                            name=title, duration=duration,
                            media=[MononobeMedia(uri=f.as_posix(), media_type=SearchType.song, bitrate=bitrate)],
                            artists=[artist_model], album=album_model)

    def show_media(self, media_type: SearchType, identifier: str) -> Optional[MononobeSong]:
        path = base64.b64decode(identifier).decode()
        f = Path(path)
        return self._get_model_from_file(f)

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
            self._songs.append(self._get_model_from_file(f))

    @staticmethod
    def get_meta_or_empty(file, key: str) -> str:
        try:
            return str(file[key])
        except KeyError:
            return ''

    def load_metadata(self, f: Path) -> Tuple[str, str, str, int, int]:
        mime, _ = guess_type(f)
        file = mutagen.File(f)
        title = ''
        artist = ''
        album = ''

        if mime.endswith('mpeg'):
            title = self.get_meta_or_empty(file, 'TIT2')
            artist = self.get_meta_or_empty(file, 'TPE1')
            album = self.get_meta_or_empty(file, 'TALB')
        elif mime.endswith('flac'):
            title = str(file['title'][0])
            artist = str(file['artist'][0])
            album = str(file['album'][0])

        if title == '':
            title = f.stem

        return title, artist, album, file.info.length * 1000, file.info.bitrate

    @staticmethod
    def filter_song_by_name(song: MononobeSong, keyword: str) -> bool:
        return song.name.lower().find(keyword.lower()) != -1

    def keyword_search(self, search_type: SearchType, keyword: str, page: int, page_size: int) \
            -> Union[MononobePagination[MononobeModel], Awaitable[MononobePagination[MononobeModel]]]:
        data = list(filter(lambda s: self.filter_song_by_name(s, keyword), self._songs))
        return MononobePagination(page=page, page_size=page_size, total=len(data),
                                  data=data[page_size * (page - 1):page_size])

    def get_media(self, search_type: SearchType, identifier: str, bitrate: int = None) -> Optional[MononobeMedia]:
        if search_type == SearchType.song:
            song = self._get_model_from_file(Path(base64.b64decode(identifier).decode()))
            assert len(song.media) > 0
            return song.media[0]
        raise MononobeNotImplemented()


if __name__ == '__main__':
    LocalProvider()
