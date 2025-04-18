import asyncio
import json
import re
import shutil
import signal
import sys
import time
import uuid
from pathlib import Path
from typing import List, Dict, Optional
import logging

import aiofiles
import httpx
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from tqdm.asyncio import tqdm
from urllib3.exceptions import ResponseError

from nexadataset import settings
from nexadataset.services.models import DownloadTask, DownloadResult
from nexadataset.services.auth import AuthService

logger = logging.getLogger(__name__)


class DownloadError(Exception):
    """自定义下载异常"""


class AsyncDownloadService:
    def __init__(self, config):
        self.auth_service = AuthService()
        self.client = httpx.AsyncClient(
            base_url=settings.BASE_URL,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
        )
        self.config = config
        self._semaphore = asyncio.Semaphore(config.max_concurrency)
        self._shutdown_event = asyncio.Event()
        self._setup_signal_handlers()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        await self.client.aclose()

    @retry(
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(httpx.NetworkError),
        reraise=True
    )
    async def download_file(
            self,
            dataset_repo: str,
            target_path: str,
            source_path: str,
            version_num: int,
    ) -> None:
        if not re.match(r"^nexadataset/[a-zA-Z0-9_-]+$", dataset_repo):
            raise ValueError(
                f"数据集仓库格式错误: '{dataset_repo}'。"
                "必须使用 'nexadataset/数据集名称' 格式，"
                "其中数据集名称只能包含字母、数字、下划线和连字符。"
            )
        prefix, dataset_repo = dataset_repo.split('/')
        target_path = Path(target_path).expanduser().resolve()
        target_path = Path(target_path).expanduser().resolve()
        try:
            target_path.mkdir(parents=True, exist_ok=True)
        except FileNotFoundError as e:
            raise DownloadError(f"无法创建目录 {target_path}，父目录不存在: {e}")
        except PermissionError as e:
            raise DownloadError(f"没有权限创建目录 {target_path}，请检查用户权限: {e}")
        # 创建下载任务
        task = DownloadTask(
            dataset_repo=dataset_repo,
            source_path=source_path,
            version_num=version_num,
        )
        results = {}
        async with self._semaphore:
            # 直接处理单个任务
            task_id, result = await self._process_single_task(task, target_path)
            results[task_id] = result  # 存储结果
        return results

    def _setup_signal_handlers(self):
        if sys.platform != 'win32':
            loop = asyncio.get_event_loop()
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, self._graceful_shutdown)
        else:
            logger.info("Windows 不支持信号处理，跳过信号处理器注册")

    def _graceful_shutdown(self):
        logger.warning("收到终止信号，开始优雅关闭...")
        self._shutdown_event.set()

    async def _download_file(self, task: DownloadTask, target_path: Path, token: str,
                             file_progress: tqdm, total_progress: tqdm) -> DownloadResult:
        headers = {"Authorization": f"Bearer {token}"}
        params = {"mountPath": task.dataset_repo, "fileName": task.source_path, "versionNum": task.version_num or ""}
        if not target_path.parent.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
        file_exists_response = await self.client.get(
            url="/api/client/isFileExist",
            params=params,
            headers=headers,
        )
        file_exists = file_exists_response.json()
        if file_exists.get('code') == 200 and file_exists.get('status') == 0:
            return file_exists.get('data')
        else:
            match = re.search(r"\[(.*?)\]", file_exists.get('msg'))
            if match:
                content = match.group(1)
            raise RuntimeError(content)

        file_size = target_path.stat().st_size if target_path.exists() else 0
        if file_size > 0:
            headers["Range"] = f"bytes={file_size}-"

        async with self.client.stream("GET", "/api/client/downloadFile", params=params, headers=headers) as response:
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise DownloadError("下载失败: 未授权，请登录或检查AK/SK是否过期或是否已禁用")
                raise DownloadError(f"下载失败: {e}")

            total_size = file_size + int(response.headers.get("Content-Length", 0))
            target_path = await self._get_unique_filename(target_path)

            # 临时的文件进度条，leave=False 保证进度条下载完成后消失
            async with aiofiles.open(target_path, 'ab') as f:
                async for chunk in response.aiter_bytes(self.config.chunk_size):
                    await f.write(chunk)
                    file_progress.update(len(chunk))  # 更新文件的进度条
                    if total_progress:
                        total_progress.update(len(chunk))

            # 返回文件下载结果
            return DownloadResult(success=True, file_path=target_path, bytes_transferred=total_size)

    async def _get_file_list(self, dataset_repo: str, version_num: Optional[int], token: str) -> List[DownloadTask]:
        params = {"mountPath": dataset_repo, "versionNum": version_num}
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.get("/api/client/getFileList", params=params, headers=headers)
        try:
            response.raise_for_status()
            response_data = response.json()
            # 验证响应格式
            if response_data.get('code') == 200 and response_data.get('status') == 0:
                return response_data.get('data')
            else:
                match = re.search(r"\[(.*?)\]", response_data.get('msg'))
                if match:
                    content = match.group(1)
                raise RuntimeError(content)
            if not isinstance(response_data, dict) or 'data' not in response_data:
                raise ResponseError("无效的接口响应格式")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise DownloadError("下载失败: 未授权，请登录或检查AK/SK是否过期或是否已禁用")
            raise Exception(f"下载失败: {e.response.status_code},{await e.response.aread()}")  # 视情况是否继续抛出

        file_list = response_data['data']
        tasks = []
        for file in file_list:
            # 构建完整的文件路径
            file_path = file['filePath'].rstrip('/')
            file_name = f"{file['fileName']}.{file['extendName']}" if file['extendName'] else file['fileName']
            source_path = f"{file_path}/{file_name}"
            # 创建下载任务
            task = DownloadTask(
                dataset_repo=dataset_repo,
                source_path=source_path,
                version_num=version_num,
                file_size=file['fileSize']
            )
            tasks.append(task)

        return tasks

    async def execute_download(self, dataset_repo: str, version_num: Optional[int] = None,
                               target_path: Path = Path('downloads')) -> Dict[str, DownloadResult]:
        if not re.match(r"^nexadataset/[a-zA-Z0-9_-]+$", dataset_repo):
            raise ValueError(
                f"数据集仓库格式错误: '{dataset_repo}'。"
                "必须使用 'nexadataset/数据集名称' 格式，"
                "其中数据集名称只能包含字母、数字、下划线和连字符。"
            )

        prefix, dataset_repo = dataset_repo.split('/')
        target_path = Path(target_path).expanduser().resolve().joinpath(dataset_repo)
        try:
            if target_path.exists():
                raise FileExistsError(f"数据集目录已存在:{dataset_repo}")
            try:
                target_path.mkdir(parents=True, exist_ok=True)
            except FileNotFoundError as e:
                raise DownloadError(f"无法创建目录 {target_path}，父目录不存在: {e}")
            except PermissionError as e:
                raise DownloadError(f"没有权限创建目录 {target_path}，请检查用户权限: {e}")
            token = await self.auth_service.get_token()
            file_list = await self._get_file_list(dataset_repo, version_num, token)
            results = {}
            # 计算所有文件的总大小
            total_size = sum([file.file_size for file in file_list])  # 你需要确保文件大小在文件列表中
            # 创建总进度条
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Total Download Progress",
                      dynamic_ncols=True) as total_progress:
                results = {}
                async with self._semaphore:
                    coros = [self._process_single_task(task, target_path, total_progress) for task in file_list]
                    for future in asyncio.as_completed(coros):
                        task_id, result = await future
                        results[task_id] = result

            return results
        except Exception as e:
            try:
                if target_path.exists():
                    shutil.rmtree(target_path)
            except Exception as cleanup_error:
                print(f"[清理失败] 无法删除目录 {target_path}：{cleanup_error}")
            raise DownloadError(f"{e}")

    async def _process_single_task(self, task: DownloadTask, target_path: Path, total_progress: tqdm = None) -> tuple[
        str, DownloadResult]:
        target_file_path = target_path / Path(task.source_path.lstrip("/"))
        # 创建临时进度条显示文件下载进度
        with tqdm(total=task.file_size, unit='B', unit_scale=True, desc=f"Downloading {task.source_path}",
                  dynamic_ncols=True,
                  leave=False) as file_progress:
            result = await self._download_file(task, target_file_path, await self.auth_service.get_token(),
                                               file_progress, total_progress)
        # 更新总进度条
        return f"{task.dataset_repo}/{task.source_path}_{int(time.time())}_{uuid.uuid4()}", result

    @staticmethod
    async def _get_unique_filename(target_path: Path) -> Path:
        base = target_path.stem  # 获取文件名（不带扩展名）
        extension = target_path.suffix  # 获取扩展名
        counter = 1
        # 构造新的文件名，直到没有冲突
        while target_path.exists():
            target_path = target_path.with_name(f"{base}({counter}){extension}")
            counter += 1
        return target_path
