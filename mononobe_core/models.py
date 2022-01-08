import datetime
from math import ceil
from typing import List, Optional, TypeVar, Generic, Dict, Type

from pydantic import BaseModel

from mononobe_core.enums import SearchType

T = TypeVar('T')


class MononobeModel(BaseModel):
    id: str
    provider: str


class MononobeMedia(BaseModel):
    media_type: SearchType
    bitrate: int
    uri: Optional[str]


class MononobeSong(MononobeModel):
    class Artist(MononobeModel):
        name: str
        image: Optional[str]

    class Album(MononobeModel):
        name: str
        image: Optional[str]

    name: str
    artists: Optional[List[Artist]]
    album: Optional[Album]
    duration: int
    media: Optional[List[MononobeMedia]]

    @property
    def duration_str(self) -> str:
        return str(datetime.timedelta(seconds=self.duration))

    @property
    def artists_name(self) -> str:
        if self.artists is None:
            return ''
        names = []
        for a in self.artists:
            names.append(a.name)
        return ','.join(names)

    @property
    def album_name(self) -> str:
        if self.album is None:
            return ''
        return self.album.name


class MononobeResponse(BaseModel):
    status_code: int
    headers: Dict[str, str]
    raw: bytes
    text: Optional[str]

    def parse_model(self, model_class: Type[BaseModel]) -> BaseModel:
        return model_class.parse_raw(self.raw)


class MononobePagination(BaseModel, Generic[T]):
    page: int
    page_size: int
    total: Optional[int]

    data: List[T]

    @property
    def total_page(self) -> Optional[int]:
        if self.total is None:
            return None
        return ceil(self.total / self.page_size)

    @property
    def next_page(self) -> Optional[int]:
        if self.total is None:
            return self.page + 1
        return None if self.page >= self.total_page else self.page + 1
