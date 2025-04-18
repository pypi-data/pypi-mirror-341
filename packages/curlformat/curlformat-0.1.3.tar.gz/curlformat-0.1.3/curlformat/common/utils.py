# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, Union

# Constants
BASE_INDENT = " " * 4

# Command line argument parser
parser = argparse.ArgumentParser(description='Parse curl commands into Python code')
parser.add_argument('command', help='The curl command')
parser.add_argument('url', help='The URL to request')
parser.add_argument('-d', '--data', help='HTTP POST data')
parser.add_argument('-b', '--data-binary', '--data-raw', default=None, help='Binary POST data')
parser.add_argument('-X', default='', help='HTTP request method')
parser.add_argument('-H', '--header', action='append', default=[], help='Headers')
parser.add_argument('--compressed', action='store_true', help='Request compressed response')
parser.add_argument('-k', '--insecure', action='store_true', help='Allow insecure connections')
parser.add_argument('--user', '-u', default=(), help='Server user and password')
parser.add_argument('-i', '--include', action='store_true', help='Include protocol response headers')
parser.add_argument('-s', '--silent', action='store_true', help='Silent mode')
parser.add_argument('-x', '--proxy', default={}, help='Use proxy')
parser.add_argument('-U', '--proxy-user', default='', help='Proxy user and password')


@dataclass
class ParsedContext:
    """Data class to store parsed curl command information."""
    method: str
    url: str
    data: Optional[str]
    headers: Dict[str, str]
    cookies: Dict[str, str]
    verify: bool
    auth: Union[Tuple[str, str], Tuple]
    proxy: Dict[str, str]


def normalize_newlines(multiline_text: str) -> str:
    """Normalize newlines in curl commands to handle line continuations.

    Args:
        multiline_text: The curl command that may contain line continuations

    Returns:
        A string with line continuations removed
    """
    return multiline_text.replace(" \\\n", " ")


def dict_to_pretty_string(the_dict: Dict[str, str], indent: int = 4) -> str:
    """Convert a dictionary to a pretty string representation.

    Args:
        the_dict: The dictionary to convert
        indent: The number of spaces to indent

    Returns:
        A string representation of the dictionary
    """
    if not the_dict:
        return "{}"

    # Format with consistent indentation and line breaks
    lines = ["{"]
    for i, (key, value) in enumerate(sorted(the_dict.items())):
        comma = "," if i < len(the_dict) - 1 else ""
        lines.append(f"{' ' * (indent + 4)}\"{key}\": \"{value}\"{comma}")
    lines.append(f"{' ' * indent}}}")

    return "\n".join(lines)
