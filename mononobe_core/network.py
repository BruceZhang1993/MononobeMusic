from http.cookiejar import MozillaCookieJar, Cookie

import httpx

from mononobe_core.consts import MONONOBE_CACHE_COOKIEFILE
from mononobe_core.models import MononobeResponse


class MononobeClient:
    _instance: 'MononobeClient' = None

    @classmethod
    def init(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def close(cls):
        if cls._instance is not None:
            cls._instance._cookie.save()
            cls._instance._client.close()

    def __init__(self):
        if not MONONOBE_CACHE_COOKIEFILE.parent.exists():
            MONONOBE_CACHE_COOKIEFILE.parent.mkdir(parents=True, exist_ok=True)
        self._cookie = MozillaCookieJar(MONONOBE_CACHE_COOKIEFILE)
        self._client = httpx.Client(cookies=self._cookie)

    def set_header(self, header: dict):
        self._client.headers.update(header)

    def set_cookie(self, cookie: Cookie):
        self._cookie.set_cookie(cookie)

    def get(self, url: str, *, params: dict = None):
        response = self._client.get(url, params=params, allow_redirects=True)
        return MononobeResponse(status_code=response.status_code, headers=response.headers.items(),
                                raw=response.content, text=response.text)


class MononobeAsyncClient:
    _instance: 'MononobeAsyncClient' = None

    @classmethod
    def init(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    async def close(cls):
        if cls._instance is not None:
            cls._instance._cookie.save()
            await cls._instance._client.aclose()

    def __init__(self):
        if not MONONOBE_CACHE_COOKIEFILE.parent.exists():
            MONONOBE_CACHE_COOKIEFILE.parent.mkdir(parents=True, exist_ok=True)
        self._cookie = MozillaCookieJar(MONONOBE_CACHE_COOKIEFILE)
        self._client = httpx.AsyncClient(cookies=self._cookie)

    def set_header(self, header: dict):
        self._client.headers.update(header)

    def set_cookie(self, cookie: Cookie):
        self._cookie.set_cookie(cookie)

    async def get(self, url: str, *, params: dict = None):
        response = await self._client.get(url, params=params, allow_redirects=True)
        return MononobeResponse(status_code=response.status_code, headers=response.headers.items(),
                                raw=response.content, text=response.text)

    async def post(self, url: str, *, params: dict = None, data: dict = None, json: dict = None):
        response = await self._client.post(url, params=params, data=data, json=json, allow_redirects=True)
        return MononobeResponse(status_code=response.status_code, headers=response.headers.items(),
                                raw=response.content, text=response.text)
