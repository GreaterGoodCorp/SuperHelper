# This module defines helper functions regarding I/O operations.
import sys

# Click is used to print messages (and errors)
import click


def print_error(message, *, fp=sys.stderr, colour="bright_red"):
    """Prints MESSAGE as an error to FP with color COLOUR."""
    click.secho(f"ERROR: {message}", fp, color=colour)
    return


def print_message(message, *, fp=sys.stdout, **kwargs):
    """Print a message."""
    click.secho(message, file=fp, **kwargs)
