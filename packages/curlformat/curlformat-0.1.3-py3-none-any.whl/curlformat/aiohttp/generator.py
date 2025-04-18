# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, List

from ..common import ParsedContext, dict_to_pretty_string


def generate_aiohttp_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate Python aiohttp code from a ParsedContext object.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the aiohttp call

    Returns:
        A string containing Python code that uses the aiohttp library
    """
    # Import statement for aiohttp
    import_statement = "import aiohttp\nimport asyncio\n\n"

    # Session parameters
    session_params = _get_session_params(parsed_context)

    # Request parameters
    request_params = _get_request_params(parsed_context, kwargs)

    # Format the code
    code = _format_code(parsed_context, session_params, request_params)

    return import_statement + code


def _get_session_params(parsed_context: ParsedContext) -> List[str]:
    """Get session parameters from the parsed context.

    Args:
        parsed_context: The parsed curl command

    Returns:
        A list of session parameters
    """
    session_params = []

    # Handle cookies
    if parsed_context.cookies:
        cookies_token = f"cookies={dict_to_pretty_string(parsed_context.cookies)}"
        session_params.append(cookies_token)

    # Handle auth
    if parsed_context.auth and parsed_context.auth != ():
        auth_token = f"auth=aiohttp.BasicAuth('{parsed_context.auth[0]}', '{parsed_context.auth[1] if len(parsed_context.auth) > 1 else ''}')"
        session_params.append(auth_token)

    return session_params


def _get_request_params(parsed_context: ParsedContext, kwargs: Dict[str, Any]) -> List[str]:
    """Get request parameters from the parsed context.

    Args:
        parsed_context: The parsed curl command
        kwargs: Additional keyword arguments

    Returns:
        A list of request parameters
    """
    request_params = []

    # Handle method and URL
    method = parsed_context.method.upper()
    url = parsed_context.url

    # Handle data
    if parsed_context.data:
        data_token = f"data='{parsed_context.data}'"
        request_params.append(data_token)

    # Handle headers
    if parsed_context.headers:
        headers_token = f"headers={dict_to_pretty_string(parsed_context.headers)}"
        request_params.append(headers_token)

    # Handle SSL verification
    if not parsed_context.verify:
        ssl_token = "ssl=False"
        request_params.append(ssl_token)

    # Handle proxy
    if parsed_context.proxy:
        # aiohttp uses a different proxy format
        proxy_url = None
        if "http" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["http"]
        elif "https" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["https"]

        if proxy_url:
            proxy_token = f"proxy='{proxy_url}'"
            request_params.append(proxy_token)

    # Handle additional kwargs
    for k, v in sorted(kwargs.items()):
        request_params.append(f"{k}={v}")

    return request_params


def _format_code(parsed_context: ParsedContext, session_params: List[str], request_params: List[str]) -> str:
    """Format the aiohttp code.

    Args:
        parsed_context: The parsed curl command
        session_params: List of session parameters
        request_params: List of request parameters

    Returns:
        The formatted aiohttp code
    """
    method = parsed_context.method.upper()
    url = parsed_context.url

    # Format session parameters with proper indentation
    session_params_str = ""
    if session_params:
        session_params_str = ",\n        ".join(session_params)
        session_params_str = f"\n        {session_params_str}\n    "

    # Format request parameters with proper indentation
    request_params_str = ""
    if request_params:
        request_params_str = ",\n            ".join(request_params)
        request_params_str = f",\n            {request_params_str}"

    # Create the async function with improved formatting
    code = f"""async def fetch():
    # Create an aiohttp session
    async with aiohttp.ClientSession({session_params_str}) as session:
        # Make the request
        async with session.{parsed_context.method}(
            url="{url}"{request_params_str}
        ) as response:
            # Handle the response
            print(f"Status Code: {{response.status}}")
            print(f"Headers: {{response.headers}}")
            print("Response Body:")
            text = await response.text()
            print(text)

            return text


async def main():
    result = await fetch()
    return result


if __name__ == "__main__":
    asyncio.run(main())
"""

    return code
