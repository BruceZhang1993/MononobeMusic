import asyncio
import sys

import click

from mononobe_api import Provider
from mononobe_cli.utils import coro
from mononobe_core.enums import SearchType


@click.command()
@click.option('--source', '-s', required=True, type=click.Choice(['local', 'netease'], case_sensitive=False),
              help='provider source')
@click.argument('keyword')
@coro
async def search(keyword: str, source: str):
    """Search for KEYWORD

    KEYWORD is the string to search for.

    \b
    :param keyword: the string to search for
    :type keyword: str
    :param source: provider source
    :type source: str
    """
    provider = Provider.init(source)
    if provider is None:
        click.echo(f'Unknown provider: {source}')
        sys.exit(3)
    result = provider.keyword_search(SearchType.song, keyword, 1, 20)
    if asyncio.iscoroutine(result):
        result = await result
    for r in result.data:
        media_uri = ''
        if r.media is not None:
            media_uri = r.media[0].uri
        if len(r.id) <= 7:
            print(f'{r.id}\t\t{r.name} - {r.artists_name} - {r.album_name}\t{media_uri}')
        else:
            print(f'{r.id}\t{r.name} - {r.artists_name} - {r.album_name}\t{media_uri}')
