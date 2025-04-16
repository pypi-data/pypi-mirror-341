"""CLI (Command Line Interface) of OE Python Template Example."""

import sys

import typer

from .constants import MODULES_TO_INSTRUMENT
from .utils import __version__, boot, console, get_logger, prepare_cli

boot(MODULES_TO_INSTRUMENT)
logger = get_logger(__name__)

cli = typer.Typer(help="Command Line Interface of ")
prepare_cli(cli, f"🧠 OE Python Template Example v{__version__} - built with love in Berlin 🐻")

if __name__ == "__main__":  # pragma: no cover
    try:
        cli()
    except Exception as e:  # noqa: BLE001
        logger.critical("Fatal error occurred: %s", e)
        console.print(f"Fatal error occurred: {e}", style="error")
        sys.exit(1)
