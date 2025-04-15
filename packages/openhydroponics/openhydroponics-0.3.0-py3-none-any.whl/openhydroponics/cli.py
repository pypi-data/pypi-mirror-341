import asyncio
import functools
from typing import Optional, Tuple
import click

from openhydroponics.base.endpoint import Endpoint, EndpointClass
from openhydroponics.dbus import NodeManager, Node


class KeyValueType(click.ParamType):
    name = "key=value"

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Tuple[str, str]:
        """
        Parses a 'key=value' string into a (key, value) tuple.
        """
        try:
            # Split only on the first '='
            key, val = value.split("=", 1)
            key = key.strip()
            val = val.strip()
            if not key or not val:  # Ensure neither part is empty after stripping
                raise ValueError("Both key and value are required.")
            return key, val
        except ValueError:
            # Use self.fail for Click-specific error handling
            self.fail(
                f"'{value}' is not a valid key=value string.",
                param,
                ctx,
            )


def make_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    auto_envvar_prefix="HYPO",
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--node",
    type=click.UUID,
    help="Node UUID. If not set, this is read from the environmental variable HYPO_NODE",
)
@click.pass_context
def cli(ctx, node):
    ctx.ensure_object(dict)
    ctx.obj["node"] = node


@cli.group()
def config():
    """Get and set node configuration"""


@config.command(name="set")
@click.argument("endpoint", type=int)
@click.argument("config", type=KeyValueType(), nargs=-1, metavar="name=value")
@click.pass_context
@make_sync
async def config_set(ctx, endpoint, config):
    """Set node endpoint configuration"""
    nm = NodeManager()
    await nm.init()

    config = dict(config)
    node: Node = await nm.request_node(ctx.obj["node"])
    if not node:
        click.echo("Could not find node")
        return
    endpoint: Endpoint = node.get_endpoint(endpoint)
    if not endpoint:
        click.echo("Could not find endpoint")
        return
    try:
        await endpoint.set_config(config)
    except Exception as e:
        click.echo(f"Error setting config: {e}")


@cli.command()
@click.pass_context
@make_sync
async def ls(ctx):
    """List nodes"""
    nm = NodeManager()
    await nm.init()
    async for node in nm:
        click.echo(f"Node {node.uuid}:")
        for endpoint in node:
            click.echo(
                f" - EP{endpoint.endpoint_id} {endpoint.ENDPOINT_CLASS.name}: {endpoint}"
            )


@cli.group()
@click.pass_context
@make_sync
async def output(ctx):
    """Node endpoint commands"""


@output.command(name="set")
@click.argument("endpoint", type=int)
@click.argument("value", type=float)
@click.pass_context
@make_sync
async def output_set(ctx, endpoint: int, value: float):
    """Set node endpoint output"""
    nm = NodeManager()
    await nm.init()
    node: Node = await nm.request_node(ctx.obj["node"])
    if not node:
        click.echo("Could not find node")
        return
    endpoint: Endpoint = node.get_endpoint(endpoint)
    if not endpoint:
        click.echo("Could not find endpoint")
        return
    if endpoint.ENDPOINT_CLASS != EndpointClass.Output:
        click.echo(f"Endpoint {endpoint} is not an output endpoint")
        return
    await endpoint.set(value)


if __name__ == "__main__":
    cli()
