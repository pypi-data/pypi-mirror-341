import re

import httpx
from httpx import HTTPStatusError, RequestError

from nexadataset.services.auth import AuthService


class DatasetInfo:
    def __init__(self):
        self.auth_service = AuthService()
        self.client = httpx.AsyncClient(
            base_url=self.auth_service.base_url,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
        )

    async def info(self, dataset_repo: str) -> dict:
        if not re.match(r"^nexadataset/[a-zA-Z0-9_-]+$", dataset_repo):
            raise ValueError(
                f"数据集仓库格式错误: '{dataset_repo}'。"
                "必须使用 'nexadataset/数据集名称' 格式，"
                "其中数据集名称只能包含字母、数字、下划线和连字符。"
            )

        try:
            prefix, dataset_repo = dataset_repo.split('/')
            token = await self.auth_service.get_token()
            response = await self.client.get(
                url="/api/client/info",
                params={"mountPath": dataset_repo},
                headers={"Authorization": f"Bearer {token}"},
            )

            response.raise_for_status()
            result = response.json()
            if result.get('code') == 200 and result.get('status') == 0:
                return result.get('data')
            else:
                match = re.search(r"\[(.*?)\]", result.get('msg'))
                if match:
                    content = match.group(1)
                raise RuntimeError(content)
        except HTTPStatusError as e:
            if e.response.status_code == 401:
                raise RuntimeError("下载失败: 未授权，请登录或检查AK/SK是否过期或是否已禁用")
            # 服务端返回了非 2xx 响应
            raise RuntimeError(f"服务请求失败（状态码 {e.response.status_code}）: {e.response.text}") from e

        except RequestError as e:
            # 网络错误，如连接失败、超时等
            raise RuntimeError(f"请求异常：{str(e)}") from e

        except Exception as e:
            # 其他错误
            raise RuntimeError(f"获取数据集信息时出现错误：{str(e)}") from e
