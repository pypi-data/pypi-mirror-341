# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, List

from ..common import ParsedContext, dict_to_pretty_string


def generate_requests_go_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate Python code from a ParsedContext object using the requests-go package.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the requests-go call

    Returns:
        A string containing Python code that uses the requests-go package
    """
    # Build request parameters
    request_params = _get_request_params(parsed_context, kwargs)

    # Format the code
    code = _format_request(parsed_context, request_params)

    return code


def _get_request_params(parsed_context: ParsedContext, kwargs: Dict[str, Any]) -> List[str]:
    """Get request parameters from the parsed context.

    Args:
        parsed_context: The parsed curl command
        kwargs: Additional keyword arguments

    Returns:
        A list of request parameters
    """
    request_params = []

    # Add default TLS configuration
    tls_config_token = """tls_config={
            "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24,0",
            "h2": "1:65536,2:0,3:1000,4:6291456,6:262144|15663105|0|m,a,s,p",
            "headers": {
                "order": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45",
                "special_headers": {}
            }
        }"""
    request_params.append(tls_config_token)

    # Handle data
    if parsed_context.data:
        data_token = f"data='''{parsed_context.data}'''"
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
    """Format the requests-go code.

    Args:
        parsed_context: The parsed curl command
        request_params: List of request parameters

    Returns:
        The formatted requests-go code
    """
    # Format the parameters with proper indentation
    params_str = ""
    if request_params:
        params_str = ",\n        ".join(request_params)
        params_str = f",\n        {params_str}"

    # Format the code
    code = f"""import requests_go

# Make request using requests-go
response = requests_go.{parsed_context.method}(
    url="{parsed_context.url}"{params_str}
)

# Print response information
print(f"Status Code: {{response.status_code}}")
print(f"Headers: {{response.headers}}")
print("Response Body:")
print(response.text)

# You can also access the response as JSON if applicable
try:
    json_data = response.json()
    print("\\nJSON Response:")
    print(json_data)
except ValueError:
    print("\\nResponse is not valid JSON")
"""

    return code
