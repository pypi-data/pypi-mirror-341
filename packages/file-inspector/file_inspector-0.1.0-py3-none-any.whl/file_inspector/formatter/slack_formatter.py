# slack_formatter.py

from typing import Dict
import pandas as pd


def format_file_info(info: Dict) -> str:
    return (
        f"📂 *파일 정보*\n"
        f"• 이름: `{info.get('file_name')}`\n"
        f"• 경로: `{info.get('file_path')}`\n"
        f"• 확장자: `{info.get('file_extension')}`\n"
        f"• 크기: `{info.get('file_size')}` bytes\n"
        f"• 인코딩: `{info.get('encoding')}`\n"
        f"• 구분자: `{info.get('delimiter')}`\n"
        f"• MIME 타입: `{info.get('mime_type')}`\n"
        f"• 생성일: `{info.get('created_at')}`\n"
        f"• 수정일: `{info.get('modified_at')}`\n"
        f"• 압축 여부: {'✅' if info.get('is_compressed') else '❌'}\n"
    )


def format_df_info(df: pd.DataFrame) -> str:
    return (
        f"📊 *데이터프레임 정보*\n"
        f"• 행 개수: `{df.shape[0]}`\n"
        f"• 열 개수: `{df.shape[1]}`\n"
        f"• 열 목록: `{', '.join(df.columns)}`\n"
    )


def format_slack_message(file_info: Dict, df: pd.DataFrame) -> str:
    sections = []
    if file_info:
        sections.append(format_file_info(file_info))
    if df is not None:
        sections.append(format_df_info(df))
    return "\n".join(sections)
