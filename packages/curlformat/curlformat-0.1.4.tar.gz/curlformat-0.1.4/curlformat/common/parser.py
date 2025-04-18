# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import shlex
from collections import OrderedDict
from typing import Dict

from .utils import ParsedContext, normalize_newlines, parser


def parse_context(curl_command: str) -> ParsedContext:
    """Parse a curl command into a ParsedContext object.

    Args:
        curl_command: The curl command to parse

    Returns:
        A ParsedContext object containing the parsed curl command
    """
    method = "get"

    try:
        tokens = shlex.split(normalize_newlines(curl_command))
        parsed_args = parser.parse_args(tokens)

        post_data = parsed_args.data or parsed_args.data_binary
        if post_data:
            method = 'post'

        if parsed_args.X:
            method = parsed_args.X.lower()

        cookie_dict = OrderedDict()
        quoted_headers = OrderedDict()

        # Process cookies from -b/--cookie flag
        if parsed_args.cookie:
            try:
                # Use a more robust cookie parsing method
                cookie_pairs = parsed_args.cookie.split(';')
                for pair in cookie_pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        cookie_dict[key.strip()] = value.strip()
            except Exception:
                # Handle malformed cookie
                pass

        for curl_header in parsed_args.header:
            if curl_header.startswith(':'):
                occurrence = [m.start() for m in re.finditer(':', curl_header)]
                if len(occurrence) > 1:
                    header_key, header_value = curl_header[:occurrence[1]], curl_header[occurrence[1] + 1:]
                else:
                    # Handle malformed header
                    continue
            else:
                try:
                    header_key, header_value = curl_header.split(":", 1)
                except ValueError:
                    # Handle malformed header
                    continue

            if header_key.lower().strip("$") == 'cookie':
                try:
                    # Use a more robust cookie parsing method
                    cookie_pairs = header_value.split(';')
                    for pair in cookie_pairs:
                        if '=' in pair:
                            key, value = pair.split('=', 1)
                            cookie_dict[key.strip()] = value.strip()
                except Exception:
                    # Handle malformed cookie
                    pass
            else:
                quoted_headers[header_key] = header_value.strip()

        # Add auth
        user = parsed_args.user
        if parsed_args.user and isinstance(parsed_args.user, str):
            user = tuple(user.split(':', 1)) if ':' in user else (user, '')

        # Add proxy and its authentication if it's available
        proxies = {}
        if parsed_args.proxy and parsed_args.proxy_user:
            proxies = _create_proxies(parsed_args.proxy, parsed_args.proxy_user)
        elif parsed_args.proxy:
            proxies = _create_proxies(parsed_args.proxy)

        return ParsedContext(
            method=method,
            url=parsed_args.url,
            data=post_data,
            headers=quoted_headers,
            cookies=cookie_dict,
            verify=not parsed_args.insecure,  # Note: verify is the opposite of insecure
            auth=user,
            proxy=proxies,
        )
    except Exception as e:
        raise ValueError(f"Failed to parse curl command: {e}")


def _create_proxies(proxy: str, proxy_user: str = None) -> Dict[str, str]:
    """Create proxy dictionary based on the proxy and proxy_user.

    Args:
        proxy: The proxy URL
        proxy_user: The proxy user and password (optional)

    Returns:
        A dictionary containing the proxy configuration for requests/httpx
    """
    # For requests/httpx
    if proxy_user:
        return {
            "http": f"http://{proxy_user}@{proxy}/",
            "https": f"http://{proxy_user}@{proxy}/",
        }
    else:
        return {
            "http": f"http://{proxy}/",
            "https": f"http://{proxy}/",
        }
