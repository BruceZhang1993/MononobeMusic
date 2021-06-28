import importlib
from pathlib import Path
from typing import List, Optional

import click
from click import Context, Command


class MononobeCli(click.MultiCommand):

    def list_commands(self, ctx: Context) -> List[str]:
        commands = []
        for f in Path(__file__).parent.iterdir():
            if f.name.startswith('__') or f.name.startswith('_') or not f.name.endswith('.py'):
                continue
            commands.append(f.stem)
        return commands

    def get_command(self, ctx: Context, cmd_name: str) -> Optional[Command]:
        module = importlib.import_module(f'mononobe_cli.{cmd_name}')
        if hasattr(module, cmd_name):
            return getattr(module, cmd_name)


@click.command(cls=MononobeCli)
def run():
    pass
