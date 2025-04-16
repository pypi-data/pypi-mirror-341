from typing import Literal, Dict
import zipfile
import os
from pathlib import Path
import json

import oss2
from oss2 import Bucket
from rich.console import Console
from rich.table import Table
from jsonargparse import auto_cli


console = Console()


def zip_all_files(dir, zipFile, pre_dir):
    """递归压缩文件夹下的所有文件
    参数:
    - dir: 要压缩的文件夹路径
    - zipFile: zipfile对象
    - pre_dir: 压缩文件根目录
    """
    for f in os.listdir(dir):
        absFile = os.path.join(dir, f)  # 子文件的绝对路径
        pre_d = os.path.join(pre_dir, f)
        if os.path.isdir(absFile):  # 判断是文件夹，继续深度读取。
            zipFile.write(absFile, pre_d)  # 在zip文件中创建文件夹
            zip_all_files(absFile, zipFile, pre_dir=pre_d)  # 递归操作
        else:  # 判断是普通文件，直接写到zip文件中。
            zipFile.write(absFile, pre_d)


class OSSStorer:
    """阿里云oss对象存储"""

    def __init__(
        self,
        access_key_id: str | None = None,
        access_key_secret: str | None = None,
        cache_dir: str | Path = Path().home() / ".cache" / "d-oss",
    ):
        super().__init__()
        auth_file = Path(cache_dir) / "auth.json"
        if auth_file.exists():
            with open(auth_file, "r") as f:
                auth: Dict = json.load(f)
                access_key_id = auth.get("access_key_id")
                access_key_secret = auth.get("access_key_secret")
        if access_key_id is None:
            access_key_id = os.getenv("OSS_ACCESS_KEY_ID")
        if access_key_secret is None:
            access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET")
        if access_key_id is None or access_key_secret is None:
            console.print(
                "[bold red] access_key_id or access_key_secret is None, please set it in environment variables or pass it as arguments."
            )
        if not auth_file.exists():
            auth_file.parent.mkdir(parents=True, exist_ok=True)
            with open(auth_file, "w") as f:
                json.dump(
                    {
                        "access_key_id": access_key_id,
                        "access_key_secret": access_key_secret,
                    },
                    f,
                )
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        beijing_endpoint: str = "http://oss-cn-beijing.aliyuncs.com"
        hangzhou_endpoint: str = "http://oss-cn-hangzhou.aliyuncs.com"
        data_bucket: str = "deepset"
        model_bucket: str = "pretrained-model"
        asset_bucket: str = "deepasset"
        corpus_bucket: str = "deepcorpus"
        pipe_bucket: str = "spacy-pipeline"
        self.data_bucket = oss2.Bucket(
            self.auth, beijing_endpoint, bucket_name=data_bucket
        )
        self.model_bucket = oss2.Bucket(
            self.auth, beijing_endpoint, bucket_name=model_bucket
        )
        self.assets_bucket = oss2.Bucket(
            self.auth, beijing_endpoint, bucket_name=asset_bucket
        )
        self.corpus_bucket = oss2.Bucket(
            self.auth, hangzhou_endpoint, bucket_name=corpus_bucket
        )
        self.pipe_bucket = oss2.Bucket(
            self.auth, beijing_endpoint, bucket_name=pipe_bucket
        )

        self.buckets = {
            "data": self.data_bucket,
            "model": self.model_bucket,
            "asset": self.assets_bucket,
            "corpus": self.corpus_bucket,
            "pipeline": self.pipe_bucket,
        }

        self.cache_dir = cache_dir

    def list(self, bucket: Literal["data", "model", "asset", "corpus", "pipeline"]):
        """获取bucket下的所有文件"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(bucket)
        bucket = self.buckets.get(bucket)
        for obj in oss2.ObjectIterator(bucket):
            table.add_row(obj.key)
        console.print(table)

    def upload(
        self, file: str, bucket: Literal["data", "model", "asset", "corpus", "pipeline"]
    ):
        """上传文件或者目录到bucket
        - file: 要上传的文件路径
        - bucket: 要上传到的bucket
        """
        file_path: Path = Path(file)
        if not file_path.exists():
            console.print(f"[bold red] file {file} not exists!")
            return
        bucket_obj: oss2.Bucket = self.buckets.get(bucket)
        if file_path.is_dir():
            file_zip_path = file_path.name + ".zip"
            with zipfile.ZipFile(file=file_zip_path, mode="w") as z:
                zip_all_files(file_path, z, file_path)
            try:
                with console.status(
                    f"[bold red]upload {file_path} to {bucket}", spinner="aesthetic"
                ):
                    bucket_obj.put_object_from_file(
                        key=file_zip_path, filename=file_zip_path
                    )
                    console.print(
                        f"[bold red]upload {file_path} to {bucket} succeeded!"
                    )
            except Exception as e:
                console.print(
                    f"[bold red]upload {file_path} to {bucket} failed with error: {e}"
                )
            if os.path.exists(file_zip_path):
                os.remove(path=file_zip_path)

    def download(
        self,
        file: str,
        bucket: Literal["data", "model", "asset", "corpus", "pipeline"],
        save_dir: str | None = None,
    ):
        ""
        """下载数据集
        - dataset: 数据集名称
        - localpath: 下载到本地的路径 默认为./datasets/
        """
        if save_dir is None:
            save_dir = bucket
        save_dir: Path = Path(save_dir)
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)
        bucket_obj: Bucket = self.buckets.get(bucket)
        file_path = save_dir / file
        if not file_path.exists():
            try:
                with console.status(
                    f"[bold red]download {file} from {bucket}", spinner="aesthetic"
                ):
                    bucket_obj.get_object_to_file(key=file, filename=file_path)
                    with zipfile.ZipFile(file=file_path, mode="r") as zf:
                        zf.extractall(path=save_dir)
                    console.print(
                        f"[bold red]downloaded {file} to {save_dir} succeeded!"
                    )
            except Exception:
                console.print(f"[bold red]downloaded {file} to {save_dir} failed!")
            finally:
                if os.path.exists(file_path):
                    os.remove(path=file_path)

    def delete(
        self, file: str, bucket: Literal["data", "model", "asset", "corpus", "pipeline"]
    ):
        """删除文件或者目录"""
        bucket_obj: Bucket = self.buckets.get(bucket)
        if bucket_obj.object_exists(file):
            bucket_obj.delete_object(file)
            console.print(f"[bold red]delete {file} succeed")
        else:
            console.print(f"[bold red]delete {file} failed, file not exists")


def run():
    auto_cli(OSSStorer)
