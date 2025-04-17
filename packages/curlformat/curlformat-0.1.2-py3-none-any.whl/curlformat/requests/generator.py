# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict

from ..common import BASE_INDENT, ParsedContext, dict_to_pretty_string


def generate_requests_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate Python requests code from a ParsedContext object.
    
    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the requests call
        
    Returns:
        A string containing Python code that uses the requests library
    """
    # Handle data
    data_token = ''
    if parsed_context.data:
        data_token = f"{BASE_INDENT}data='{parsed_context.data}',\n"

    # Handle verify
    verify_token = ''
    if not parsed_context.verify:
        verify_token = f"\n{BASE_INDENT}verify=False"

    # Handle additional kwargs
    requests_kwargs = ''
    for k, v in sorted(kwargs.items()):
        requests_kwargs += f"{BASE_INDENT}{k}={v},\n"

    # Handle auth
    auth_data = f"{BASE_INDENT}auth={parsed_context.auth}"
    
    # Handle proxies
    proxy_token = ''
    if parsed_context.proxy:
        proxy_token = f"\n{BASE_INDENT}proxies={parsed_context.proxy}"

    # Create formatter dictionary
    formatter = {
        'method': parsed_context.method,
        'url': parsed_context.url,
        'data_token': data_token,
        'headers_token': f"{BASE_INDENT}headers={dict_to_pretty_string(parsed_context.headers)}",
        'cookies_token': f"{BASE_INDENT}cookies={dict_to_pretty_string(parsed_context.cookies)}",
        'security_token': verify_token,
        'requests_kwargs': requests_kwargs,
        'auth': auth_data,
        'proxies': proxy_token
    }

    # Generate code
    return """requests.{method}("{url}",
{requests_kwargs}{data_token}{headers_token},
{cookies_token},
{auth},{proxies},{security_token}
)""".format(**formatter)
