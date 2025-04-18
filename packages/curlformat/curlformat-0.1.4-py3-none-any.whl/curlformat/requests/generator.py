# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, List

from ..common import ParsedContext, dict_to_pretty_string, is_json


def generate_requests_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate Python requests code from a ParsedContext object.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the requests call

    Returns:
        A string containing Python code that uses the requests library
    """
    # Import statement
    import_statement = "import requests\n\n"

    # Build request parameters
    request_params = _get_request_params(parsed_context, kwargs)

    # Format the code
    code = _format_request(parsed_context, request_params)

    return import_statement + code


def _get_request_params(parsed_context: ParsedContext, kwargs: Dict[str, Any]) -> List[str]:
    """Get request parameters from the parsed context.

    Args:
        parsed_context: The parsed curl command
        kwargs: Additional keyword arguments

    Returns:
        A list of request parameters
    """
    request_params = []

    # Handle data
    if parsed_context.data:
        if is_json(parsed_context.data):
            # If data is JSON, use json parameter instead of data
            json_data = parsed_context.data.strip()
            data_token = f"json={json_data}"
        else:
            data_token = f"data='{parsed_context.data}'"
        request_params.append(data_token)

    # Handle headers
    if parsed_context.headers:
        headers_token = f"headers={dict_to_pretty_string(parsed_context.headers)}"
        request_params.append(headers_token)

    # Handle cookies
    if parsed_context.cookies:
        cookies_token = f"cookies={dict_to_pretty_string(parsed_context.cookies)}"
        request_params.append(cookies_token)

    # Handle auth
    if parsed_context.auth:
        auth_token = f"auth={parsed_context.auth}"
        request_params.append(auth_token)

    # Handle verify
    if not parsed_context.verify:
        verify_token = "verify=False"
        request_params.append(verify_token)

    # Handle proxies
    if parsed_context.proxy:
        proxies_token = f"proxies={parsed_context.proxy}"
        request_params.append(proxies_token)

    # Handle additional kwargs
    for k, v in sorted(kwargs.items()):
        request_params.append(f"{k}={v}")

    return request_params


def _format_request(parsed_context: ParsedContext, request_params: List[str]) -> str:
    """Format the requests code.

    Args:
        parsed_context: The parsed curl command
        request_params: List of request parameters

    Returns:
        The formatted requests code
    """
    # Format the parameters with proper indentation
    params_str = ""
    if request_params:
        params_str = ",\n        ".join(request_params)
        params_str = f",\n        {params_str}"

    # Format the code
    code = f"""# Make request using requests
response = requests.{parsed_context.method}(
    url="{parsed_context.url}"{params_str}
)

# Print response information
print(f"Status Code: {{response.status_code}}")
print(f"Headers: {{response.headers}}")
print("Response Body:")
print(response.text)
"""

    return code
