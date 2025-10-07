from typing import Dict

from datetime import datetime

import bcrypt, re, uuid


def encode(param: str):
    hash_param = bcrypt.hashpw(param.encode(), bcrypt.gensalt())
    return hash_param.decode()


def now_datatime():
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    now = datetime.now().strftime(time_format)
    return datetime.strptime(now, time_format)


def create_uuid4() -> uuid.UUID:
    return uuid.uuid4()


def clean_data(data: Dict[str, str]) -> Dict[str, str]:
    for key, value in data.items():
        if isinstance(data[key], str):
            data[key] = re.sub(r"<.*?>", "", value)
            data[key] = re.sub(r"\s+", " ", data[key]).strip()

    return data


def pagination_info(page: int, per_page: int, total: int):
    total_pages = (total + per_page - 1) // per_page

    return {
        "status": "success",
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
    }
