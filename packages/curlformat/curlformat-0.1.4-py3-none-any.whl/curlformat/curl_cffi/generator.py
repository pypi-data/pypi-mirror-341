# -*- coding: utf-8 -*-
from __future__ import annotations

from enum import Enum
import random
from typing import Any, Dict, List, Tuple

from ..common import ParsedContext, dict_to_pretty_string, is_json


class CurlCffiMode(Enum):
    """Enum for curl_cffi mode (sync or async)."""
    SYNC = "sync"
    ASYNC = "async"


def _get_random_browser_impersonate() -> Dict[str, str]:
    """Generate random browser impersonation options.

    Returns:
        A dictionary containing browser impersonation options
    """
    # List of available browsers in curl_cffi
    browsers = [
        "chrome",
        "chrome110",
        "chrome99",
        "chrome107",
        "chrome104",
        "chrome100",
        "firefox",
        "firefox102",
        "firefox91",
        "firefox100",
        "safari",
        "safari15",
        "safari15_3",
        "safari15_5",
        "edge",
        "edge99",
        "edge101"
    ]

    # Randomly select a browser
    browser = random.choice(browsers)

    return {"browser_name": browser}


def generate_curl_cffi_code(parsed_context: ParsedContext, mode: CurlCffiMode = CurlCffiMode.SYNC, **kwargs: Any) -> str:
    """Generate Python curl_cffi code from a ParsedContext object.

    Args:
        parsed_context: The parsed curl command
        mode: The curl_cffi mode (sync or async)
        **kwargs: Additional keyword arguments to pass to the curl_cffi call

    Returns:
        A string containing Python code that uses the curl_cffi library
    """
    if mode == CurlCffiMode.ASYNC:
        return _generate_async_code(parsed_context, **kwargs)
    else:
        return _generate_sync_code(parsed_context, **kwargs)


def _generate_sync_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate synchronous Python curl_cffi code.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the curl_cffi call

    Returns:
        A string containing synchronous Python code that uses the curl_cffi library
    """
    # Import statement
    import_statement = "import random\nfrom curl_cffi import requests\nfrom curl_cffi.impersonate import ImpersonateConfig\n\n"

    # Get random browser impersonation
    browser_impersonate = _get_random_browser_impersonate()

    # Build request parameters
    params = _build_request_params(parsed_context, **kwargs)

    # Format the code
    code = f"""# List of available browsers in curl_cffi
browsers = [
    "chrome", "chrome110", "chrome99", "chrome107", "chrome104", "chrome100",
    "firefox", "firefox102", "firefox91", "firefox100",
    "safari", "safari15", "safari15_3", "safari15_5",
    "edge", "edge99", "edge101"
]

# Randomly select a browser for impersonation
browser_name = random.choice(browsers)
print(f"Impersonating {{browser_name}} browser")

# Configure impersonation
impersonate_config = ImpersonateConfig(browser_name=browser_name)

# Make request using curl_cffi with browser impersonation
response = requests.{parsed_context.method}(
    url="{parsed_context.url}",
    impersonate=impersonate_config,
{params}
)

# Print response information
print(f"Status Code: {{response.status_code}}")
print(f"Headers: {{response.headers}}")
print("Response Body:")
print(response.text)
"""

    return import_statement + code


def _generate_async_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate asynchronous Python curl_cffi code.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the curl_cffi call

    Returns:
        A string containing asynchronous Python code that uses the curl_cffi library
    """
    # Import statement
    import_statement = "import asyncio\nimport random\nfrom curl_cffi.requests import AsyncSession\nfrom curl_cffi.impersonate import ImpersonateConfig\n\n"

    # Get random browser impersonation
    browser_impersonate = _get_random_browser_impersonate()

    # Build request parameters
    params = _build_request_params(parsed_context, **kwargs)

    # Format the code
    code = f"""# List of available browsers in curl_cffi
browsers = [
    "chrome", "chrome110", "chrome99", "chrome107", "chrome104", "chrome100",
    "firefox", "firefox102", "firefox91", "firefox100",
    "safari", "safari15", "safari15_3", "safari15_5",
    "edge", "edge99", "edge101"
]

async def make_request():
    # Randomly select a browser for impersonation
    browser_name = random.choice(browsers)
    print(f"Impersonating {{browser_name}} browser")

    # Configure impersonation
    impersonate_config = ImpersonateConfig(browser_name=browser_name)

    async with AsyncSession() as session:
        response = await session.{parsed_context.method}(
            url="{parsed_context.url}",
            impersonate=impersonate_config,
{params}
        )

        # Print response information
        print(f"Status Code: {{response.status_code}}")
        print(f"Headers: {{response.headers}}")
        print("Response Body:")
        print(response.text)

        return response


async def main():
    response = await make_request()
    return response


if __name__ == "__main__":
    asyncio.run(main())
"""

    return import_statement + code


def _build_request_params(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Build request parameters for curl_cffi.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments

    Returns:
        A string containing the formatted request parameters
    """
    params = []

    # Handle headers
    if parsed_context.headers:
        headers_str = dict_to_pretty_string(parsed_context.headers)
        params.append(f"        headers={headers_str}")

    # Handle data
    if parsed_context.data:
        if is_json(parsed_context.data):
            # If data is JSON, use json parameter instead of data
            json_data = parsed_context.data.strip()
            params.append(f"        json={json_data}")
        else:
            params.append(f"        data='''{parsed_context.data}'''")

    # Handle cookies
    if parsed_context.cookies:
        cookies_str = dict_to_pretty_string(parsed_context.cookies)
        params.append(f"        cookies={cookies_str}")

    # Handle SSL verification
    if not parsed_context.verify:
        params.append("        verify=False")

    # Handle authentication
    if parsed_context.auth and parsed_context.auth != ():
        if len(parsed_context.auth) > 1:
            params.append(f"        auth=('{parsed_context.auth[0]}', '{parsed_context.auth[1]}')")
        else:
            params.append(f"        auth=('{parsed_context.auth[0]}', '')")

    # Handle proxy
    if parsed_context.proxy:
        proxy_url = None
        if "http" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["http"]
        elif "https" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["https"]

        if proxy_url:
            params.append(f"        proxies={{'http': '{proxy_url}', 'https': '{proxy_url}'}}")

    # Handle additional kwargs
    for key, value in sorted(kwargs.items()):
        params.append(f"        {key}={value}")

    return ",\n".join(params)
