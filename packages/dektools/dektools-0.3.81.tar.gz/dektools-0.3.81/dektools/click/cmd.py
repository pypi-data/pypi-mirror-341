import typer
from typing import Annotated, Optional, List
from ..typer import command_mixin, annotation
from . import git as git_command

app = typer.Typer(add_completion=False)

app.add_typer(git_command.app, name='git')


@command_mixin(app)
def retry(
        args,
        retry_times: Annotated[Optional[int], annotation.Option('--times')] = -1,
        cmd: Annotated[Optional[List[str]], annotation.Option()] = None
):
    from ..shell import shell_retry
    if cmd:
        commands = cmd
    else:
        commands = args
    shell_retry(commands, retry_times if retry_times >= 0 else None)


@command_mixin(app)
def headless(args, sync: Annotated[bool, annotation.Option("--sync/--no-sync")] = True):
    from ..shell import shell_command_nt_headless
    shell_command_nt_headless(args, sync)


@command_mixin(app)
def admin(args):
    from ..shell import shell_command_nt_as_admin
    shell_command_nt_as_admin(args)


@command_mixin(app, name='timeout')
def _timeout(args, timeout):
    from ..shell import shell_timeout
    shell_timeout(args, int(float(timeout)))
