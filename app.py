import click
from commands import star_rail_sync_roles as command_star_rail_sync_roles


# conda activate ./.env


@click.group(help='米哈游游戏自动化任务')
def cli():
    pass


@cli.command(help='米游社角色同步')
def star_rail_sync_roles():
    command_star_rail_sync_roles()


if __name__ == '__main__':
    cli()
