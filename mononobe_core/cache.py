from hashlib import sha256
from pathlib import Path
from typing import Optional

from mononobe_core.consts import MONONOBE_CACHE_RESOURCE_DIR
from mononobe_core.network import MononobeClient, MononobeAsyncClient


class CacheManager:
    _instance: 'CacheManager' = None

    @classmethod
    def init(cls) -> 'CacheManager':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        MONONOBE_CACHE_RESOURCE_DIR.mkdir(parents=True, exist_ok=True)
        self.files = [f for f in MONONOBE_CACHE_RESOURCE_DIR.iterdir()]

    def get(self, uri: str) -> Optional[Path]:
        key = sha256(uri.encode()).hexdigest()
        return list(filter(lambda f: f.stem == key, self.files)).pop()

    def save(self, uri: str):
        key = sha256(uri.encode()).hexdigest()
        data = MononobeClient.init().get(uri).raw
        with (MONONOBE_CACHE_RESOURCE_DIR / key).open('wb') as f:
            f.write(data)
            f.flush()
        self.files.append(MONONOBE_CACHE_RESOURCE_DIR / key)

    async def async_save(self, uri: str):
        key = sha256(uri.encode()).hexdigest()
        data = (await MononobeAsyncClient.init().get(uri)).raw
        with (MONONOBE_CACHE_RESOURCE_DIR / key).open('wb') as f:
            f.write(data)
            f.flush()
        self.files.append(MONONOBE_CACHE_RESOURCE_DIR / key)


if __name__ == '__main__':
    print(CacheManager.init().get('https://baidu.com'))
