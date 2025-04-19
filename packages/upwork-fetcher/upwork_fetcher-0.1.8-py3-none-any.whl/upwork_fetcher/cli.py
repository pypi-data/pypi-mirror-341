import click

from upwork_fetcher.config import load_config
from upwork_fetcher.commands import fetch, setup


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    # print("Hello from upwork_fetcher")

    config = load_config()

    # upwork_fetcher_directory = config.get("upwork_dir", str(CONFIG_DIR))

    # if not os.path.exists(upwork_fetcher_directory):
    #     os.makedirs(upwork_fetcher_directory)

    # click.echo(f"upwork_fetcher directory: {upwork_fetcher_directory}")
    click.echo(f"config: {config}")

    ctx.obj = config


cli.add_command(fetch)
cli.add_command(setup)


# async def async_main():
#     await cli.main(standalone_mode=False)


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(async_main())
