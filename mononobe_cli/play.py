import asyncio
import sys

import click

from mononobe_api import Provider
from mononobe_cli.utils import coro
from mononobe_core.enums import SearchType
from mononobe_core.player import Player


@click.command()
@click.option('--source', '-s', required=True, type=click.Choice(['local', 'netease'], case_sensitive=False),
              help='provider source')
@click.argument('identifier')
@coro
async def play(identifier: str, source: str):
    """Play the track of IDENTIFIER

    IDENTIFIER is the track ID.

    \b
    :param identifier: id of the track
    :type identifier: str
    :param source: provider source
    :type source: str
    """
    player = Player.init('vlc')
    song = Provider.init(source).show_media(SearchType.song, identifier)
    if asyncio.iscoroutine(song):
        song = await song
    if song is None:
        sys.exit(6)
    media = Provider.init(source).get_media(SearchType.song, identifier)
    if asyncio.iscoroutine(media):
        media = await media
    if media is None:
        sys.exit(6)
    song.media = [media]
    await player.async_play_song(song)
