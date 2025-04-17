# -*- coding: utf-8 -*-
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

from ..common import ParsedContext, dict_to_pretty_string


class CurlCffiMode(Enum):
    """Enum for curl_cffi mode (sync or async)."""
    SYNC = "sync"
    ASYNC = "async"


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
    import_statement = "from curl_cffi import requests\n\n"
    
    # Build request parameters
    params = _build_request_params(parsed_context, **kwargs)
    
    # Format the code
    code = f"""# Make request using curl_cffi
response = requests.{parsed_context.method}(
    url="{parsed_context.url}",
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
    import_statement = "import asyncio\nfrom curl_cffi.requests import AsyncSession\n\n"
    
    # Build request parameters
    params = _build_request_params(parsed_context, **kwargs)
    
    # Format the code
    code = f"""async def make_request():
    async with AsyncSession() as session:
        response = await session.{parsed_context.method}(
            url="{parsed_context.url}",
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
        params.append(f"    headers={headers_str}")
    
    # Handle data
    if parsed_context.data:
        params.append(f"    data='{parsed_context.data}'")
    
    # Handle cookies
    if parsed_context.cookies:
        cookies_str = dict_to_pretty_string(parsed_context.cookies)
        params.append(f"    cookies={cookies_str}")
    
    # Handle SSL verification
    if not parsed_context.verify:
        params.append("    verify=False")
    
    # Handle authentication
    if parsed_context.auth and parsed_context.auth != ():
        if len(parsed_context.auth) > 1:
            params.append(f"    auth=('{parsed_context.auth[0]}', '{parsed_context.auth[1]}')")
        else:
            params.append(f"    auth=('{parsed_context.auth[0]}', '')")
    
    # Handle proxy
    if parsed_context.proxy:
        proxy_url = None
        if "http" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["http"]
        elif "https" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["https"]
        
        if proxy_url:
            params.append(f"    proxies={{'http': '{proxy_url}', 'https': '{proxy_url}'}}")
    
    # Handle additional kwargs
    for key, value in kwargs.items():
        params.append(f"    {key}={value}")
    
    return ",\n".join(params)
