import asyncio
import os
import sys

import click
import yaml
from click_repl import register_repl

from learn_raft.service.cluster_manager_service import ClusterManagerService
from learn_raft.starters.cluster_manager_server_starter import ClusterManagerServerStarter
from learn_raft.starters.raft_server_starter import RaftServerStarter
from learn_raft_kvstore.client.TextClient import TextClient
from learn_raft_kvstore.service.kv_server import KVServer


class Config:
    def __init__(self, home, config):
        self.home = home
        # TODO Fix me to source this from a file
        # self.config = {"raft_ports": [5090, 5091, 5092], "kv_port": 8080}
        self.config = config
        self.verbose = False

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo(f"  config[{key}] = {value}", file=sys.stderr)

    def __repr__(self):
        return f"<Config {self.config}>"


pass_config = click.make_pass_decorator(Config)


@click.group()
@click.option(
    "--config-file",
    default="./learn_raft_kvstore/config/conf.yaml",
    type=click.Path()
)
@click.option(
    "--home",
    envvar="RAFT_HOME",
    default=".raft",
    metavar="PATH",
    help="Changes the root folder of the raft store.",
)
@click.version_option("1.0")
@click.pass_context
def cli(ctx, home, config_file):  # pragma: no cover
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    # ctx.obj = Config(config)
    ctx.obj = Config(os.path.abspath(home), config)


@cli.command()
@click.argument("method")
@click.argument("arg")
@pass_config
def client(config, method, arg):
    click.echo(f"Started KV server client connection to server 5090")
    txclient = TextClient(5090)
    if method == "request_vote":
        txclient.request_vote(arg)
    elif method == "get":
        txclient.get(arg)


@cli.command()
@click.argument("configs", required=True, metavar="KEY=VALUE", nargs=-1, type=str)
@pass_config
def set_config(config, configs):  # pragma: no cover
    for config in configs:
        key, value = config.split("=")
        config.config[key] = value


# @cli.command()
# @pass_config
# def start_all(config):
#     raft_server_configs = config.config["raft_servers"]
#     raft_servers = []
#     for server_config in raft_server_configs:
#         server = Server(id=int(server_config["id"]), host=server_config["host"], port=int(server_config["port"]))
#         raft_servers.append(server)
#
#     asyncio.run(kv_grpc_server.start(config.config))

@cli.command()
@pass_config
@click.option("-i", "--id", required=True, type=int)
@click.option("-h", "--host", required=True, type=str)
@click.option("-p", "--port", required=True, type=int)
def start_cluster_manager(config, id, host, port):
    cluster_manager = ClusterManagerServerStarter()
    asyncio.run(cluster_manager.start(id, host, port, config.config))


@cli.command()
@pass_config
@click.option("-i", "--id", required=True, type=int)
@click.option("-h", "--host", required=True, type=str)
@click.option("-p", "--port", required=True, type=int)
@click.option("-c", "--cluster-manager-ip", required=True, type=str)
def start_raft_node(config, id, host, port, cluster_manager_ip):
    raft_server = RaftServerStarter(cluster_manager_ip)
    asyncio.run(raft_server.start(id, host, port, config.config))


@cli.command()
@pass_config
@click.option("-i", "--id", required=True, type=int)
@click.option("-h", "--host", required=True, type=str)
@click.option("-p", "--port", required=True, type=int)
@click.option("-c", "cluster_manager_ip", required=True, type=str)
def start_kv_node(config, id, host, port, cluster_manager_ip):
    kv_server = KVServer(cluster_manager_ip)
    kv_server.add_kv_node(id, host, port, config.config)


@cli.command()
@click.argument("root")
@click.confirmation_option()
@pass_config
def stop(config, root):
    click.echo(f"Stopping server with identifier xxxxx on port xxxxx {config.home}/{root}")
    click.echo("Stopped the Raft server dropped!")


register_repl(cli)
cli()
