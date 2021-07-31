import base64
import binascii
import json
import os

from Crypto.Cipher import AES

from mononobe_api.netease.schema import SearchResultResponse, SongUrlResponse
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
    WE_BASE = 'http://music.163.com/weapi'

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

    async def song_detail(self, music_id: str):
        uri = f'{self.BASE}/song/detail/?id={music_id}&ids=[{music_id}]'
        response = await self._client.get(uri)
        print(response.text)

    async def song_url(self, music_id: str) -> SongUrlResponse:
        uri = f'{self.WE_BASE}/song/enhance/player/url'
        data = {
            'ids': [music_id],
            'br': 320000,
            'csrf_token': self._client.get_cookie('__csrf')
        }
        payload = self.encrypt_request(data)
        response = await self._client.post(uri, data=payload)
        return response.parse_model(SongUrlResponse)

    def _create_aes_key(self, size):
        return (''.join([hex(b)[2:] for b in os.urandom(size)]))[0:16]

    def _aes_encrypt(self, text, key):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(bytes(key, 'utf-8'), 2, b'0102030405060708')
        enc_text = encryptor.encrypt(bytes(text, 'utf-8'))
        enc_text_encode = base64.b64encode(enc_text)
        return enc_text_encode

    def _rsa_encrypt(self, text):
        e = '010001'
        n = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615' \
            'bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf' \
            '695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46' \
            'bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b' \
            '8e289dc6935b3ece0462db0a22b8e7'
        reverse_text = text[::-1]
        encrypted_text = pow(int(binascii.hexlify(reverse_text), 16),
                             int(e, 16), int(n, 16))
        return format(encrypted_text, "x").zfill(256)

    def encrypt_request(self, data):
        text = json.dumps(data)
        first_aes_key = '0CoJUm6Qyw8W8jud'
        second_aes_key = self._create_aes_key(16)
        enc_text = self._aes_encrypt(
            self._aes_encrypt(text, first_aes_key).decode('ascii'),
            second_aes_key).decode('ascii')
        enc_aes_key = self._rsa_encrypt(second_aes_key.encode('ascii'))
        payload = {
            'params': enc_text,
            'encSecKey': enc_aes_key,
        }
        return payload


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(NeteaseApi().song_url('1824222230')))
