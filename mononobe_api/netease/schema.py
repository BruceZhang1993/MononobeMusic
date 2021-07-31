from typing import List, Union, Optional

from pydantic import BaseModel, validator

from mononobe_core.enums import SearchType
from mononobe_core.models import MononobeSong, MononobeMedia

SOURCE = 'netease'


class DefaultModel(BaseModel):
    pass


class SearchArtist(DefaultModel):
    id: int = 0
    name: str
    img1v1Url: str = ''

    def to_model(self):
        return MononobeSong.Artist(id=str(self.id), name=self.name, provider=SOURCE)


class SearchAlbum(DefaultModel):
    id: int = 0
    name: str
    artist: SearchArtist
    picId: int
    copyrightId: int
    publishTime: int


class SearchSong(DefaultModel):
    id: int = 0
    name: str
    artists: List[SearchArtist]
    album: SearchAlbum
    duration: int
    copyrightId: int
    mvid: int
    fee: int

    def to_model(self):
        return MononobeSong(id=str(self.id), provider=SOURCE, name=self.name, duration=self.duration,
                            album=MononobeSong.Album(id=str(self.album.id), provider=SOURCE, name=self.album.name),
                            artists=[a.to_model() for a in self.artists])


class SongSearchResult(DefaultModel):
    hasMore: bool
    songCount: int
    songs: List[SearchSong]

    def to_model(self):
        return [s.to_model() for s in self.songs]


class ArtistSearchResult(DefaultModel):
    hasMore: bool
    artistCount: int
    artists: List[SearchArtist]

    def to_model(self):
        return [s.to_model() for s in self.artists]


class SongUrlData(DefaultModel):
    id: int
    url: Optional[str]
    br: int

    def to_model(self):
        return MononobeMedia(id=str(self.id), provider='netease', media_type=SearchType.song, bitrate=self.br, uri=self.url)


class SearchResultResponse(DefaultModel):
    code: int
    result: Union[SongSearchResult, ArtistSearchResult]


class SongDetailResponse(DefaultModel):
    code: int


class SongUrlResponse(DefaultModel):
    code: int
    data: List[SongUrlData]
