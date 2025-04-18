import asyncio
import json
import logging
from datetime import datetime, timezone

import jwt
import httpx
import aiofiles
from typing import Optional
from aiofiles import os
from jwt import PyJWTError

from nexadataset import settings

CONFIG_PATH = settings.CONFIG_PATH.expanduser()  # 避免路径错误，测试时放在 /tmp，可修改为 ~/.nexadataset/config.json


async def delete_credentials():
    """删除本地凭证文件"""
    try:
        # 先检查文件是否存在（同步方式，因为检查操作很快）
        if not os.path.exists(CONFIG_PATH):
            return False

        # 异步删除文件
        try:
            await aiofiles.os.remove(str(CONFIG_PATH))
            return True
        except PermissionError:
            print("错误：没有删除文件的权限")
        except Exception as e:
            print(f"删除文件时出错: {e}")

        return False

    except Exception as e:
        print(f"操作过程中发生意外错误: {e}")
        return False


async def load_credentials():
    """加载本地凭证"""
    try:
        async with aiofiles.open(CONFIG_PATH, "r") as f:
            content = await f.read()
            return json.loads(content)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"读取凭证失败: {e}")
        return None


async def save_credentials(data):
    """保存凭证到本地"""
    try:
        if not CONFIG_PATH.parent.exists():
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(CONFIG_PATH, "w") as f:
            await f.write(json.dumps(data, indent=4))
    except Exception as e:
        logging.error(f"保存凭证失败: {e}")


async def login(key: str, secret: str) -> None:
    """
    登录方法，验证 key 和 secret。

    :param key: 用户密钥
    :param secret: 用户密钥对应的密码
    """
    async with AuthService() as auth:
        result = await auth.aksk(key, secret)  # ❗ 这里要加 await
        if result and result["code"] == 200 and result["status"] == 0:
            await save_credentials(result["data"])  # ❗ 这里也是异步
            logging.info("Login successful.")


def login_sync(key: str, secret: str):
    asyncio.run(login(key, secret))


async def get_jwt_expiry(token: str) -> datetime | None:
    """Extract expiration time from JWT token.

    Args:
        token: JWT token string

    Returns:
        datetime object of expiration if present and valid, None otherwise
    """
    try:
        # Decode token without verification
        decoded = jwt.decode(
            token,
            options={
                "verify_signature": False,
                "verify_exp": False  # We'll handle expiration manually
            }
        )

        # Get expiration timestamp
        exp_timestamp = decoded.get('exp')
        if exp_timestamp is None:
            return None

        # Convert to datetime (UTC)
        return datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    except PyJWTError as e:
        print(f"Token decoding failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error processing token: {e}")
        return None


class AuthService:
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.token: Optional[str] = None
        self.expires_time = 0
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def fetch_token(self, access_key, secret_key) -> Optional[dict]:
        """请求新的 token"""
        if not access_key or not secret_key:
            logging.error("缺少 access_key 或 secret_key，无法获取 token")
            return None

        url = "/api/public/client/token"
        data = {
            "accessKey": access_key,
            "secretKey": secret_key
        }

        try:
            response = await self.client.get(url, params=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP 错误: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"请求错误: {e}")
        return None

    async def aksk(self, access_key, secret_key) -> Optional[dict]:
        """请求新的 token"""
        if not access_key or not secret_key:
            logging.error("缺少 access_key 或 secret_key，无法获取 token")
            return None
        url = "/api/public/client/aksk"
        data = {
            "accessKey": access_key,
            "secretKey": secret_key
        }
        try:
            response = await self.client.get(url, params=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP 错误: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"请求错误: {e}")
        return None

    async def get_token(self) -> Optional[str]:
        """获取token（自动处理刷新逻辑）"""
        if self.token:
            try:
                expire_time = await get_jwt_expiry(self.token)
                if expire_time and expire_time > datetime.now(timezone.utc):
                    return self.token
            except Exception as e:
                print(f"Token验证异常: {e}")

        # 2. 尝试从本地加载凭证
        credentials = await load_credentials()
        if not credentials:
            raise ValueError("未找到有效凭证，请先设置登录")

        # 3. 验证凭证完整性
        required_keys = {"accessKey", "secretKey"}
        if not required_keys.issubset(credentials.keys()):
            raise ValueError("凭证文件缺少必要字段,请重新登录")

        # 4. 获取新token
        try:
            new_token_data = await self.fetch_token(
                credentials["accessKey"],
                credentials["secretKey"]
            )

            if not new_token_data or new_token_data.get("code") != 200:
                raise ValueError("获取新token失败")

            self.token = new_token_data["data"]["access_token"]

            return self.token

        except Exception as e:
            return None

    async def close(self):
        """关闭 httpx.AsyncClient 资源"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
