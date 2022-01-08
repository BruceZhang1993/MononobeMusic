import asyncio

import click

from mononobe_api import Provider
from mononobe_cli.utils import coro
from mononobe_core.enums import SearchType


@click.command()
@click.option('--source', '-s', required=True, type=click.Choice(['local', 'netease'], case_sensitive=False),
              help='provider source')
@click.argument('identifier')
@coro
async def show(identifier: str, source: str):
    song = Provider.init(source).show_media(SearchType.song, identifier)
    if asyncio.iscoroutine(song):
        song = await song
    print(f'ID:       {song.id}')
    print(f'Name:     {song.name}')
    print(f'Duration: {song.duration_str}')
    print(f'Album:    {song.album.name}')
    print(f'Artists:  {[a.name for a in song.artists]}')
    print(f'Cover:    {song.album.image}')
