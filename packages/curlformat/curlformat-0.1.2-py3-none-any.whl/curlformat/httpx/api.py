# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from ..common import parse_context
from .generator import generate_httpx_code, HttpxMode


def parse(curl_command: str, async_mode: bool = False, **kwargs: Any) -> str:
    """Parse a curl command into a Python httpx code snippet.

    Args:
        curl_command: The curl command to parse
        async_mode: Whether to generate async code
        **kwargs: Additional keyword arguments to pass to the httpx call

    Returns:
        A string containing Python code that uses the httpx library
    """
    parsed_context = parse_context(curl_command)
    mode = HttpxMode.ASYNC if async_mode else HttpxMode.SYNC
    return generate_httpx_code(parsed_context, mode=mode, **kwargs)


def parse_async(curl_command: str, **kwargs: Any) -> str:
    """Parse a curl command into an async Python httpx code snippet.

    Args:
        curl_command: The curl command to parse
        **kwargs: Additional keyword arguments to pass to the httpx call

    Returns:
        A string containing async Python code that uses the httpx library
    """
    return parse(curl_command, async_mode=True, **kwargs)
