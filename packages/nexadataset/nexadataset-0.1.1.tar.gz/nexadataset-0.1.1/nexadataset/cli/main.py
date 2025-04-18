import click
from nexadataset.cli.download import download, login, logout, status, info
from importlib.metadata import version, PackageNotFoundError
import platform


def get_version_info() -> str:
    try:
        pkg_version = version("nexadataset")
    except PackageNotFoundError:
        pkg_version = "unknown"
    return click.style(f"""\
NexaDataset CLI 工具
---------------------
版本号     : {pkg_version}
作者       : shimingming <shimingming@zoneyet.com>
Python版本 : {platform.python_version()}
系统       : {platform.system()} {platform.release()}
""", fg='green')  # 设置文本颜色为绿色


@click.group(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="NexaDataset CLI\n\n支持数据集下载、信息查看和登录等功能。"
)
@click.version_option(
    version=get_version_info(),
    prog_name="NexaDataset CLI 工具",
    message="%(version)s",
)
def cli():
    """NexaDataset 数据集管理平台命令行工具"""
    pass


cli.add_command(download)
cli.add_command(login)
cli.add_command(logout)
cli.add_command(status)
cli.add_command(info)
