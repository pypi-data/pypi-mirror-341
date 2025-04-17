# -*- coding:utf-8 -*-
# @Function  : __init__.py
# @Author    : wjh
# @Time      : 2025-04-10
# Version    : 1.0

import os

from dotenv import load_dotenv

load_dotenv()

def getenv(key: str, default: str = None, type_: type = str):
    value = os.getenv(key, default)
    if value is None:
        return None
    try:
        return type_(value)
    except (ValueError, TypeError):
        return default