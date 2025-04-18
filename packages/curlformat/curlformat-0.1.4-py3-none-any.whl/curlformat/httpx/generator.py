# -*- coding: utf-8 -*-
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Tuple

from ..common import ParsedContext, dict_to_pretty_string, is_json


class HttpxMode(Enum):
    """Enum for httpx mode (sync or async)."""
    SYNC = "sync"
    ASYNC = "async"


def generate_httpx_code(parsed_context: ParsedContext, mode: HttpxMode = HttpxMode.SYNC, **kwargs: Any) -> str:
    """Generate Python httpx code from a ParsedContext object.

    Args:
        parsed_context: The parsed curl command
        mode: The httpx mode (sync or async)
        **kwargs: Additional keyword arguments to pass to the httpx call

    Returns:
        A string containing Python code that uses the httpx library
    """
    # Import statement for httpx
    import_statement = _get_import_statement(mode)

    if mode == HttpxMode.ASYNC:
        # For async mode, generate a complete async function
        return _generate_async_code(parsed_context, **kwargs)
    else:
        # For sync mode, generate the regular code
        # Client creation with common parameters
        client_params = _get_client_params(parsed_context)

        # Format client creation
        client_creation, indent = _format_client_creation(client_params, mode)

        # Handle request parameters
        request_params = _get_request_params(parsed_context, kwargs)

        # Format request
        request = _format_request(parsed_context, request_params, indent, mode)

        # Add response handling
        response_handling = _format_response_handling(indent)

        return import_statement + client_creation + request + response_handling


def _get_import_statement(mode: HttpxMode) -> str:
    """Get the import statement for httpx.

    Args:
        mode: The httpx mode (sync or async)

    Returns:
        The import statement
    """
    if mode == HttpxMode.ASYNC:
        return "import httpx\nimport asyncio\n\n"
    else:
        return "import httpx\n\n"


def _get_client_params(parsed_context: ParsedContext) -> List[str]:
    """Get client parameters from the parsed context.

    Args:
        parsed_context: The parsed curl command

    Returns:
        A list of client parameters
    """
    client_params = []

    # Handle cookies
    if parsed_context.cookies:
        cookies_token = f"cookies={dict_to_pretty_string(parsed_context.cookies)}"
        client_params.append(cookies_token)

    # Handle auth
    if parsed_context.auth:
        auth_token = f"auth={parsed_context.auth}"
        client_params.append(auth_token)

    # Handle verify
    if not parsed_context.verify:
        verify_token = "verify=False"
        client_params.append(verify_token)

    # Handle proxies
    if parsed_context.proxy:
        proxies_token = f"proxies={parsed_context.proxy}"
        client_params.append(proxies_token)

    return client_params


def _format_client_creation(client_params: List[str], mode: HttpxMode) -> Tuple[str, str]:
    """Format client creation code.

    Args:
        client_params: List of client parameters
        mode: The httpx mode (sync or async)

    Returns:
        A tuple containing the client creation code and the indentation
    """
    if mode == HttpxMode.ASYNC:
        if client_params:
            params_str = ",\n    ".join(client_params)
            client_creation = f"async with httpx.AsyncClient(\n    {params_str}\n) as client:\n"
        else:
            client_creation = "async with httpx.AsyncClient() as client:\n"
    else:
        if client_params:
            params_str = ",\n    ".join(client_params)
            client_creation = f"with httpx.Client(\n    {params_str}\n) as client:\n"
        else:
            client_creation = "with httpx.Client() as client:\n"

    indent = "    "
    return client_creation, indent


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

    # Handle additional kwargs
    for k, v in sorted(kwargs.items()):
        request_params.append(f"{k}={v}")

    return request_params


def _format_request(parsed_context: ParsedContext, request_params: List[str], indent: str, mode: HttpxMode) -> str:
    """Format request code.

    Args:
        parsed_context: The parsed curl command
        request_params: List of request parameters
        indent: Indentation string
        mode: The httpx mode (sync or async)

    Returns:
        The formatted request code
    """
    # Format the parameters with proper indentation
    params_str = ""
    if request_params:
        params_str = ",\n        ".join(request_params)
        params_str = f",\n        {params_str}"

    # Format the request based on mode
    if mode == HttpxMode.ASYNC:
        return f"{indent}# Make the request\n{indent}response = await client.{parsed_context.method}(\n{indent}    url=\"{parsed_context.url}\"{params_str}\n{indent})\n"
    else:
        return f"{indent}# Make the request\n{indent}response = client.{parsed_context.method}(\n{indent}    url=\"{parsed_context.url}\"{params_str}\n{indent})\n"


def _format_response_handling(indent: str) -> str:
    """Format response handling code.

    Args:
        indent: Indentation string

    Returns:
        The formatted response handling code
    """
    return f"{indent}# Handle the response\n{indent}response.raise_for_status()\n\n{indent}# Print response information\n{indent}print(f\"Status Code: {{response.status_code}}\")\n{indent}print(f\"Headers: {{response.headers}}\")\n{indent}print(\"Response Body:\")\n{indent}print(response.text)"


def _generate_async_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate async Python httpx code.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the httpx call

    Returns:
        A string containing async Python code that uses the httpx library
    """
    # Import statement
    import_statement = "import httpx\nimport asyncio\n\n"

    # Build client parameters
    client_params = []
    if parsed_context.cookies:
        client_params.append(f"cookies={dict_to_pretty_string(parsed_context.cookies)}")
    if parsed_context.auth:
        client_params.append(f"auth={parsed_context.auth}")
    if not parsed_context.verify:
        client_params.append("verify=False")
    if parsed_context.proxy:
        client_params.append(f"proxies={parsed_context.proxy}")

    # Format client parameters
    client_params_str = ""
    if client_params:
        client_params_str = ",\n        ".join(client_params)
        client_params_str = f"\n        {client_params_str}\n    "

    # Build request parameters
    request_params = []
    if parsed_context.data:
        if is_json(parsed_context.data):
            # If data is JSON, use json parameter instead of data
            json_data = parsed_context.data.strip()
            request_params.append(f"json={json_data}")
        else:
            request_params.append(f"data='{parsed_context.data}'")
    if parsed_context.headers:
        request_params.append(f"headers={dict_to_pretty_string(parsed_context.headers)}")

    # Add additional kwargs
    for k, v in sorted(kwargs.items()):
        request_params.append(f"{k}={v}")

    # Format request parameters
    request_params_str = ""
    if request_params:
        request_params_str = ",\n            ".join(request_params)
        request_params_str = f",\n            {request_params_str}"

    # Generate the async code
    code = f"""async def fetch():
    # Create an async client
    async with httpx.AsyncClient({client_params_str}) as client:
        # Make the request
        response = await client.{parsed_context.method}(
            url="{parsed_context.url}"{request_params_str}
        )

        # Handle the response
        response.raise_for_status()

        # Print response information
        print(f"Status Code: {{response.status_code}}")
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

    return import_statement + code

