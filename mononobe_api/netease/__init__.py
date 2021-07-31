from typing import Optional

from mononobe_api import Provider
from mononobe_api.netease.api import NeteaseApi
from mononobe_core.enums import SearchType
from mononobe_core.models import MononobePagination, MononobeModel, MononobeMedia


class NeteaseProvider(Provider):

    def __init__(self):
        self.api = NeteaseApi()

    async def keyword_search(self, search_type: SearchType, keyword: str, page: int, page_size: int) \
            -> MononobePagination[MononobeModel]:
        response = await self.api.keyword_search(search_type, keyword, page, page_size)
        return MononobePagination(page=page, page_size=page_size, total=response.result.songCount,
                                  data=response.result.to_model())

    async def get_media(self, search_type: SearchType, identifier: str, bitrate: int = None) -> Optional[MononobeMedia]:
        response = await self.api.song_url(identifier)
        if len(response.data) == 0:
            return None
        return response.data[0].to_model()
