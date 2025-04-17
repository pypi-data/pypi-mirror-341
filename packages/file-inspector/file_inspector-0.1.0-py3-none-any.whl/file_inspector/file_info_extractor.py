# file_info_extractor.py

from datetime import datetime
from typing import Dict
from . import utils

class FileInfoExtractor:
    """
    파일 메타 정보를 추출하는 책임을 가지는 클래스
    - 파일 존재 여부, 경로, 이름, 크기, MIME, 인코딩, 구분자, 생성/수정 시간, 압축 여부
    """

    def extract(self, file_path: str) -> Dict:
        confirm_at = datetime.now()

        if not utils.is_file_exists(file_path):
            return {
                "file_exists": False,
                "file_path": file_path,
                "confirm_at": confirm_at,
                "message": "File does not exist"
            }

        encoding = utils.detect_file_encoding(file_path)
        delimiter = utils.detect_delimiter(file_path, encoding)

        return {
            "file_exists": True,
            "file_path": file_path,
            **utils.get_file_name_and_extension(file_path),
            "file_size": utils.get_file_size(file_path),
            "confirm_at": confirm_at,
            **utils.get_file_timestamps(file_path),
            "mime_type": utils.get_file_mime_type(file_path),
            "encoding": encoding,
            "delimiter": delimiter,
            "is_compressed": utils.is_compressed_file(file_path)
        }