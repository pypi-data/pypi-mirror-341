import asyncio
import json
import traceback
from pathlib import Path

from nexadataset.services.auth import AuthService
from nexadataset.services.dataset_info import DatasetInfo
from nexadataset.services.download_service import AsyncDownloadService
from nexadataset.config import DownloadConfig


class NexaDatasetClient:
    def __init__(self, config: DownloadConfig = None):
        self.config = config or DownloadConfig()
        self.download_service = AsyncDownloadService(self.config)
        self.dataset_service = DatasetInfo()
        self.auth_service = AuthService()
        self.token = None

    def download_file(self, dataset_repo: str, target_path: str, source_path: str, version_num: int):
        """下载单个文件"""
        result = asyncio.run(
            self.download_service.download_file(
                dataset_repo=dataset_repo,
                version_num=version_num,
                target_path=Path(target_path),
                source_path=source_path
            )
        )
        return result

    def download_dataset(self, dataset_repo: str, target_path: str, version_num: int):
        """下载整个数据集"""
        results = asyncio.run(
            self.download_service.execute_download(
                dataset_repo=dataset_repo,
                version_num=version_num,
                target_path=Path(target_path)
            )
        )
        return results

    def info(self, dataset_repo: str):
        """获取数据集信息"""
        try:
            result = asyncio.run(
                self.dataset_service.info(dataset_repo=dataset_repo)
            )
            # 判断 result 是否符合预期结构
            if not result or 'data' not in result:
                raise ValueError("返回数据格式不正确")

            formatted_output = json.dumps(result['data'], indent=2, ensure_ascii=False)
            return formatted_output
        except (KeyboardInterrupt, asyncio.CancelledError):
            return "任务被取消"
        except asyncio.TimeoutError:
            return "请求超时"
        except json.JSONDecodeError:
            return "JSON 格式解析失败"
        except Exception as e:
            # 返回错误信息 + 堆栈，便于排查
            return f"获取数据集信息失败：{str(e)}\n{traceback.format_exc()}"
