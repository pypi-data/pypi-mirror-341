from enum import Enum


# 错误代码枚举类
class DownloadErrorCode(Enum):
    SUCCESS = 200
    UNAUTHORIZED = 401
    SERVER_ERROR = 500


# 错误状态枚举类
class DownloadErrorStatus(Enum):
    OK = 0
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    VALUE_ERROR = 1001


class DownloadErrorMessage(Enum):
    UNAUTHORIZED = "未授权，请登录或检查 AK/SK"
    NOT_FOUND = "未找到资源，请检查路径或版本号"
    CONFLICT = "目标文件已存在"
    INVALID_FORMAT = "数据集仓库格式不正确"
    NO_PERMISSION = "没有权限访问指定路径"
    NETWORK_ISSUE = "网络请求失败，请检查连接"
    SERVER_EXCEPTION = "服务器内部错误"
