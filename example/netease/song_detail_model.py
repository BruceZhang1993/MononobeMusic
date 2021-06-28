from typing import Any, List, Optional
from pydantic import BaseModel


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
    company: str
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


class Song(BaseModel):
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
    ringtone: str
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
    hMusic: Music
    mMusic: Music
    lMusic: Music
    bMusic: Music
    mvid: int
    rtype: int
    rurl: Any
    mp3Url: Any


class Model(BaseModel):
    songs: List[Song]
    equalizers: dict
    code: int
