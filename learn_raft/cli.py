import os
import sys

import click
from click_repl import register_repl

from learn_raft.client.TextClient import TextClient
from learn_raft.service import grpc_server


class Config:
    def __init__(self, home):
        self.home = home
        self.config = {}
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


@cli.command()
@click.argument("port")
@pass_config
def start(config, port):
    click.echo(f"Started Raft server at port: {port}")
    grpc_server.start(port)


@cli.command()
@click.argument("root")
@click.confirmation_option()
@pass_config
def stop(config, root):
    click.echo(f"Stopping server with identifier xxxxx on port xxxxx {config.home}/{root}")
    click.echo("Stopped the Raft server dropped!")


@cli.command()
@click.argument("message")
@click.argument("port")
@pass_config
def client(config, message, port):
    click.echo(f"Started Raft client connection to server at port: {port}")
    txclient = TextClient()
    txclient.start(port)
    txclient.say_hello(message)


#
# @cli.command()
# @click.argument("records", required=True, metavar="KEY=VALUE", nargs=-1, type=str)
# @pass_db
# def insert(db, records):
#     click.echo(f"Records to be inserted: {records}")
#     click.echo(f"Data inserted into : {db}")
#
#
# @cli.command()
# @click.argument("keys", required=True, nargs=-1, type=str)
# @pass_db
# def delete(db, keys):
#     click.echo(f"Keys to be deleted: {keys}")
#     click.echo(f"Data deleted from : {db}")


register_repl(cli)
cli()
