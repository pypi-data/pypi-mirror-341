# types.py

from typing import Protocol, Dict, Optional
import pandas as pd


class IFileReader(Protocol):
    def read(self, file_info: Dict) -> Optional[pd.DataFrame]:
        ...


class IFileInfoExtractor(Protocol):
    def extract(self, file_path: str) -> Dict:
        ...


class ISchemaValidator(Protocol):
    def has_columns(self, required_columns: list[str]) -> bool:
        ...

    def missing_columns(self, required_columns: list[str]) -> list[str]:
        ...
