## 打包
```bash
pip install build
python -m build
```

## 上传
```bash

twine upload --repository-url  dist/*
```
## 使用方法
### CLI
#### 安装和更新
```bash
pip install  nexadataset 
pip install  -U nexadataset   # 更新版本
```

####查看版本
```bash
nexadataset --version  

```

#### 使用
```bash
nexadataset login --access-key <ACCESS KEY> --secret-key <SECRET KEY>  #从数据集管理平台获取

nexadataset info --dataset-repo nexadataset/<dataset-repo>   # 查看数据集详情

nexadataset download --dataset-repo nexadataset/<dataset-repo> [--version-num <version-num>] --target-path <target-dir>  # 下载数据集

nexadataset download --dataset-repo nexadataset/<dataset-repo> [--version-num <version-num>] --source-path /example.txt --target-path <target-dir>   #下载数据集中的文件
```

### SDK
#### 安装和更新
```bash
pip install  nexadataset 
pip install  -U nexadataset    # 更新版本
```

#### 使用
```python
import nexadataset
nexadataset.login(ak='<Access Key>', sk='<Secret Key>') # 进行登录，输入对应的AK/SK，可在个人中心添加AK/SK

from nexadataset.dataset import info
info(dataset_repo='nexadataset/<dataset-repo>') #数据集信息查看

from nexadataset.dataset import get
get(dataset_repo='nexadataset/<dataset-repo>', target_path='/path/to/local/folder/') # 数据集下载

from nexadataset.dataset import download
download(dataset_repo='nexadataset/<dataset-repo>',source_path='/README.md', target_path='/path/to/local/folder') #数据集文件下载
```