from pydantic import BaseModel
from typing import Optional
from pathlib import Path


class DownloadTask(BaseModel):
    dataset_repo: str
    source_path: str
    version_num: Optional[int] = None
    file_size: Optional[int] = None


class DownloadResult(BaseModel):
    success: bool
    file_path: Path
    bytes_transferred: int = 0
    error: Optional[str] = None
    checksum_valid: Optional[bool] = None
