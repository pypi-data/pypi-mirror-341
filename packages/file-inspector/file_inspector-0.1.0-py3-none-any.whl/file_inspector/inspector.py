# file_inspector/inspector.py

import time
from typing import Optional, List
import pandas as pd

from .file_reader import FileReader
from .file_info_extractor import FileInfoExtractor
from .schema_validator import SchemaValidator


class FileInspectionResult:
    """
    파일 분석 결과를 담는 클래스.
    다양한 출력 포맷, 유효성 검사, 통계 분석 등의 기능 제공
    """
    def __init__(self, file_info: dict, df: Optional[pd.DataFrame], elapsed: float = 0.0):
        self.file_info = file_info
        self.df = df
        self.elapsed = elapsed

    def to_dict(self) -> dict:
        return {
            "file_info": self.file_info,
            "df_shape": self.df.shape if self.df is not None else None,
            "elapsed_time": self.elapsed
        }

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), default=str)

    def to_html(self) -> str:
        return self.df.to_html() if self.df is not None else "<p>No DataFrame available</p>"

    def to_markdown(self) -> str:
        return self.df.head().to_markdown() if self.df is not None else "No DataFrame available"

    def validate_schema(self, required_columns: List[str]) -> bool:
        if self.df is None:
            return False
        validator = SchemaValidator(self.df)
        return validator.has_columns(required_columns)

    def sample_preview(self, n: int = 5) -> Optional[pd.DataFrame]:
        return self.df.head(n) if self.df is not None else None

    def generate_summary_report(self) -> Optional[pd.DataFrame]:
        return self.df.describe(include='all') if self.df is not None else None


class FileInspector:
    """
    파일 분석 메인 진입점 클래스
    파일 정보 추출 + 파일 로딩 + 결과 생성
    """
    def __init__(self):
        self.reader = FileReader()
        self.extractor = FileInfoExtractor()

    def inspect(self, file_path: str) -> FileInspectionResult:
        start = time.time()
        file_info = self.extractor.extract(file_path)
        df = self.reader.read(file_info)
        elapsed = round(time.time() - start, 3)
        return FileInspectionResult(file_info, df, elapsed)

    def batch_inspect(self, directory_path: str) -> List[FileInspectionResult]:
        import os
        results = []
        for file_name in os.listdir(directory_path):
            full_path = os.path.join(directory_path, file_name)
            if os.path.isfile(full_path):
                results.append(self.inspect(full_path))
        return results
