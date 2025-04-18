# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from ..common import parse_context
from .generator import generate_aiohttp_code


def parse(curl_command: str, **kwargs: Any) -> str:
    """Parse a curl command into a Python aiohttp code snippet.

    Args:
        curl_command: The curl command to parse
        **kwargs: Additional keyword arguments to pass to the aiohttp call

    Returns:
        A string containing Python code that uses the aiohttp library
    """
    parsed_context = parse_context(curl_command)
    return generate_aiohttp_code(parsed_context, **kwargs)
