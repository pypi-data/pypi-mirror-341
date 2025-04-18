from nexadataset.error.error_code import DownloadErrorCode, DownloadErrorStatus


class DownloadError(Exception):
    def __init__(self, code: DownloadErrorCode, status: DownloadErrorStatus, msg: str):
        self.code = code
        self.status = status
        self.msg = msg
        super().__init__(f"[{code.value}] {status.value}: {msg}")

    def to_dict(self):
        return {
            "code": self.code.value,
            "status": self.status.value,
            "msg": self.msg,
        }
