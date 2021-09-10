from typing import List, Union, Optional, Any

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


class Artist(BaseModel):
    name: str
    id: int
    picId: int
    img1v1Id: int
    briefDesc: str
    picUrl: str
    img1v1Url: str
    albumSize: int
    alias: List
    trans: str
    musicSize: int
    topicPerson: int


class Album(BaseModel):
    name: str
    id: int
    type: str
    size: int
    picId: int
    blurPicUrl: str
    companyId: int
    pic: int
    picUrl: str
    publishTime: int
    description: str
    tags: str
    company: Optional[str]
    briefDesc: str
    artist: Artist
    songs: List
    alias: List
    status: int
    copyrightId: int
    commentThreadId: str
    artists: List[Artist]
    subType: str
    transName: Any
    onSale: bool
    mark: int
    picId_str: str


class Music(BaseModel):
    name: Any
    id: int
    size: int
    extension: str
    sr: int
    dfsId: int
    bitrate: int
    playTime: int
    volumeDelta: float


class SongDetail(DefaultModel):
    name: str
    id: int
    position: int
    alias: List
    status: int
    fee: int
    copyrightId: int
    disc: str
    no: int
    artists: List[Artist]
    album: Album
    starred: bool
    popularity: float
    score: int
    starredNum: int
    duration: int
    playedNum: int
    dayPlays: int
    hearTime: int
    ringtone: Optional[str]
    crbt: Any
    audition: Any
    copyFrom: str
    commentThreadId: str
    rtUrl: Any
    ftype: int
    rtUrls: List
    copyright: int
    transName: Any
    sign: Any
    mark: int
    originCoverType: int
    originSongSimpleData: Any
    single: int
    noCopyrightRcmd: Any
    hMusic: Optional[Music]
    mMusic: Optional[Music]
    lMusic: Optional[Music]
    bMusic: Optional[Music]
    mvid: int
    rtype: int
    rurl: Any
    mp3Url: Any

    def to_model(self) -> Optional[MononobeSong]:
        return MononobeSong(id=str(self.id), provider='netease', name=self.name, duration=self.duration,
                            artists=[MononobeSong.Artist(id=str(a.id), name=a.name, image=a.picUrl, provider='netease') for a in self.artists],
                            album=MononobeSong.Album(id=str(self.album.id), provider='netease', name=self.album.name, image=self.album.picUrl))


class SearchResultResponse(DefaultModel):
    code: int
    result: Union[SongSearchResult, ArtistSearchResult]


class SongDetailResponse(DefaultModel):
    code: int
    songs: List[SongDetail]


class SongUrlResponse(DefaultModel):
    code: int
    data: List[SongUrlData]
