""" 纯标准库读取 .env 文件，加载到 os.environ """

import os
from pathlib import Path


def load_env(file_path: Path) -> None:
    """纯标准库读取 .env 文件，加载到 os.environ"""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    value = value[1:-1]
                os.environ[key] = value
