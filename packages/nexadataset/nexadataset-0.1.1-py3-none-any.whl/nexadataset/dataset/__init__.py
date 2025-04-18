from .client import NexaDatasetClient


# 下载整个数据集
def get(dataset_repo: str, target_path: str, version_num: int | None = None):
    dataset_client = NexaDatasetClient()
    return dataset_client.download_dataset(dataset_repo, target_path, version_num)


# 下载单个文件
def download(dataset_repo: str, target_path: str, source_path: str, version_num: int | None = None):
    dataset_client = NexaDatasetClient()
    return dataset_client.download_file(dataset_repo, target_path, source_path, version_num)


def info(dataset_repo: str, ):
    dataset_client = NexaDatasetClient()
    return dataset_client.info(dataset_repo)
