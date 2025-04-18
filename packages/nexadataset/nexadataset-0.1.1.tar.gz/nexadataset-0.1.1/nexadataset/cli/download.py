import json
import os
from getpass import getpass
from pathlib import Path
import asyncio
import getpass
from typing import Optional
import click
from nexadataset.services.dataset_info import DatasetInfo
from nexadataset.services.download_service import AsyncDownloadService  # 替换成你的模块
from nexadataset.config import DownloadConfig
from nexadataset.services.auth import AuthService, CONFIG_PATH, save_credentials, delete_credentials, load_credentials


@click.option('--version', '-V', help='CLI版本信息', required=False)
def version(key: Optional[str], secret: Optional[str]):
    """查看nexadataset版本信息
    """
    # 获取缺失的凭证
    if not key:
        key = click.prompt("Key", hide_input=False)
    if not secret:
        secret = getpass.getpass("Secret: ")

    asyncio.run(_async_login(key, secret))

@click.command("login")
@click.option('--key', '-k', help='数据集管理平台的accessKey', required=False)
@click.option('--secret', '-s', help='数据集管理平台的secretKey', required=False)
def login(key: Optional[str], secret: Optional[str]):
    """登录 NexaDataset
    """
    # 获取缺失的凭证
    if not key:
        key = click.prompt("Key", hide_input=False)
    if not secret:
        secret = getpass.getpass("Secret: ")

    asyncio.run(_async_login(key, secret))


async def _async_login(key, secret):
    """异步登录逻辑"""
    async with AuthService() as auth:
        result = await auth.aksk(key, secret)  # ❗ 这里要加 await
        if result and result["code"] == 200 and result["status"] == 0:
            await save_credentials(result["data"])  # ❗ 这里也是异步
            click.echo(click.style("Login successful.", fg="green"))
        else:
            click.echo(click.style(result["msg"], fg="red"))


@click.command("logout")
def logout():
    """登出 NexaDataset"""
    if os.path.exists(CONFIG_PATH):
        asyncio.run(delete_credentials())
        click.echo(click.style("Logged out successfully.", fg="green"))
    else:
        click.echo(click.style("You are not logged in.", fg="red"))


@click.command("status")
def status():
    """检查当前登录状态"""
    credentials = asyncio.run(load_credentials())
    if credentials:
        fetch_token = asyncio.run(AuthService().fetch_token(credentials['accessKey'], credentials['secretKey']))
        if fetch_token.get('code') == 200 and fetch_token.get('status') == 0:
            click.echo(click.style("状态：登录成功", fg="green"))
        else:
            click.echo(click.style(fetch_token.get('msg'), fg="red"))
    else:
        click.echo(click.style("状态：未登录", fg="red"))


@click.command("download")
@click.option('--dataset-repo', '-D', required=True, help='数据集挂载路径')
@click.option('--version-num', '-v', required=False, type=int, help='版本号')
@click.option('--target-path', '-t', default='.', type=click.Path(file_okay=False, dir_okay=True, writable=True),
              show_default=True,
              help='目标路径（默认当前目录）'
              )
@click.option('--source-path', '-s', type=str, default=None,
              help='源文件路径（如果指定，则下载单个文件）')
def download(dataset_repo, version_num, target_path, source_path):
    """下载数据集或单个文件"""
    config = DownloadConfig()
    service = AsyncDownloadService(config)

    try:
        if source_path:
            # 下载单个文件
            results = asyncio.run(
                service.download_file(
                    dataset_repo=dataset_repo,
                    version_num=version_num,
                    target_path=Path(target_path),
                    source_path=source_path
                )
            )
            for file_name, result in results.items():
                if result.success:
                    click.echo(click.style(f"下载成功: {result.file_path}", fg="green"))
                else:
                    click.echo(click.style(f" {file_name}", fg="red"))
        else:
            # 下载整个数据集
            results = asyncio.run(
                service.execute_download(
                    dataset_repo=dataset_repo,
                    version_num=version_num,
                    target_path=Path(target_path)
                )
            )
            success = sum(1 for r in results.values() if r.success)
            click.echo(click.style(f"\n下载完成: {success} 成功, {len(results) - success} 失败",
                                   fg="green" if success else "red"))

    except KeyboardInterrupt:
        click.echo(click.style("\n下载被用户中断", fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"{str(e)}", fg="red"))


@click.command("info", help="查看数据集信息")
@click.option('--dataset-repo', '-D', required=True, help='数据集挂载路径')
def info(dataset_repo: str):
    try:
        dataset_info = DatasetInfo()
        result = asyncio.run(dataset_info.info(dataset_repo))
        formatted_output = json.dumps(result, indent=2, ensure_ascii=False)  # indent=2 美化缩进，ensure_ascii=False 显示中文
        click.echo(click.style(f"数据集信息:\n{formatted_output}", fg="green"))
    except Exception as e:
        click.echo(click.style(f"获取数据集信息失败：{str(e)}", fg="red"))
