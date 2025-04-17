# file_inspector/file_reader.py

import pandas as pd
from typing import Optional, Dict

class FileReader:
    """
    파일 확장자에 따라 pandas DataFrame으로 파일을 읽어오는 클래스.
    단일 책임 원칙(SRP)을 지켜 파일 로딩만 담당.
    """

    def read(self, file_info: Dict) -> Optional[pd.DataFrame]:
        if not file_info.get("file_exists", False):
            return None

        extension = file_info.get("file_extension")
        path = file_info.get("file_path")
        encoding = file_info.get("encoding")
        delimiter = file_info.get("delimiter")

        try:
            if extension in ['.csv', '.txt', '.tsv']:
                return pd.read_csv(path, encoding=encoding, delimiter=delimiter)
            elif extension in ['.xls', '.xlsx']:
                return pd.read_excel(path)
            elif extension == '.json':
                return pd.read_json(path)
            elif extension == '.parquet':
                return pd.read_parquet(path)
        except Exception as e:
            print(f"[FileReader Error] {e}")

        return None
