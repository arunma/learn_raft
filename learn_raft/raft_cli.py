import os
import sys

import click
from click_repl import register_repl


class Config:
    def __init__(self, home):
        self.home = home
        # TODO Fix me to source this from a file
        self.config = {"ports": [5090, 5091, 5092]}
        self.verbose = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo(f"  config[{key}] = {value}", file=sys.stderr)

    def __repr__(self):
        return f"<Config {self.home}>"


pass_config = click.make_pass_decorator(Config)


@click.group()
@click.option(
    "--home",
    envvar="RAFT_HOME",
    default=".raft",
    metavar="PATH",
    help="Changes the root folder of the raft store.",
)
@click.version_option("1.0")
@click.pass_context
def cli(ctx, home):  # pragma: no cover
    ctx.obj = Config(os.path.abspath(home))


@cli.command()
@click.argument("configs", required=True, metavar="KEY=VALUE", nargs=-1, type=str)
@pass_config
def set_config(config, configs):  # pragma: no cover
    for config in configs:
        key, value = config.split("=")
        config.config[key] = value


# @cli.command()
# @click.argument("port")
# @pass_config
# def start(config, port):
#     click.echo(f"Started Raft server at port: {port}")
#     grpc_server.start(port)


@cli.command()
@click.argument("root")
@click.confirmation_option()
@pass_config
def stop(config, root):
    click.echo(f"Stopping server with identifier xxxxx on port xxxxx {config.home}/{root}")
    click.echo("Stopped the Raft server dropped!")


register_repl(cli)
cli()
