from mononobe_api.netease.schema import SearchResultResponse
from mononobe_core.enums import SearchType
from mononobe_core.network import MononobeAsyncClient

NE_SEARCH_TYPES = {
    SearchType.song: 1,
    SearchType.album: 10,
    SearchType.artist: 100,
    SearchType.playlist: 1000
}


class NeteaseApi:
    BASE = 'https://music.163.com/api'

    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 ' \
                 'Safari/537.36'

    def __init__(self):
        self._client = MononobeAsyncClient.init()
        self._client.set_header({
            'user-agent': self.USER_AGENT,
            'referer': self.BASE,
            'host': 'music.163.com'
        })

    async def keyword_search(self, search_type: SearchType, keyword: str, page: int, page_size: int) \
            -> SearchResultResponse:
        uri = f'{self.BASE}/search/get'
        data = {
            's': keyword,
            'type': NE_SEARCH_TYPES.get(search_type, ''),
            'limit': page_size,
            'offset': page_size * (page - 1)
        }
        response = await self._client.post(uri, data=data)
        return response.parse_model(SearchResultResponse)

    async def song_detail(self, music_id):
        uri = f'{self.BASE}/song/detail/?id={music_id}&ids=[{music_id}]'
        response = await self._client.get(uri)
        print(response.text)


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(NeteaseApi().song_detail('1824222230')))
