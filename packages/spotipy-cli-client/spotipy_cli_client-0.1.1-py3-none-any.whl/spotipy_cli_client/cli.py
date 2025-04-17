import os

import click

from .spotifyCLI import SpotifyCLI

# Define scope (permissions)
SCOPE = "user-library-read user-read-playback-state user-modify-playback-state"
CONFIG_FILE = os.path.expanduser("~/.spotifyclient/config.json")


# Click CLI Setup
@click.group()
def cli():
    """Interactive CLI for Spotify."""
    pass


# Create an instance
cli_instance = SpotifyCLI(CONFIG_FILE, SCOPE)

# Register class methods as click commands
cli.add_command(click.Command("init", callback=cli_instance.init))
cli.add_command(click.Command("my_playlists", callback=cli_instance.my_playlists))
cli.add_command(click.Command("search", callback=cli_instance.search))
cli.add_command(click.Command("play", callback=cli_instance.play))
cli.add_command(click.Command("next", callback=cli_instance.play_next))
cli.add_command(click.Command("prev", callback=cli_instance.play_prev))
cli.add_command(click.Command("pause", callback=cli_instance.pause))
cli.add_command(click.Command("stop", callback=cli_instance.stop))


if __name__ == "__main__":
    cli()
