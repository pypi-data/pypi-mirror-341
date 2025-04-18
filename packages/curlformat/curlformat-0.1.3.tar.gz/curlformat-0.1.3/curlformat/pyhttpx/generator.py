# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from ..common import ParsedContext


def generate_pyhttpx_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate Python pyhttpx code from a ParsedContext object.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the pyhttpx call

    Returns:
        A string containing Python code that uses the pyhttpx library
    """
    # Import statement for pyhttpx
    import_statement = "import pyhttpx\n\n"

    # Create the code
    code = _format_code(parsed_context, **kwargs)

    return import_statement + code


def _format_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Format the pyhttpx code.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments

    Returns:
        The formatted pyhttpx code
    """
    # Use multi-line strings for better readability
    code = """# Initialize client
client = pyhttpx.HttpClient()

"""

    # Set headers
    if parsed_context.headers:
        code += "# Set headers\nheaders = {\n"
        for key, value in sorted(parsed_context.headers.items()):
            code += f"    \"{key}\": \"{value}\",\n"
        code += "}\n\n"
    else:
        code += """# No headers specified
headers = {}

"""

    # Set cookies
    if parsed_context.cookies:
        code += "# Set cookies\ncookies = {\n"
        for key, value in sorted(parsed_context.cookies.items()):
            code += f"    \"{key}\": \"{value}\",\n"
        code += "}\n\n"
        code += """# Add cookies to client
for key, value in cookies.items():
    client.add_cookie(key, value)

"""

    # Set SSL verification
    if not parsed_context.verify:
        code += """# Disable SSL verification
client.verify_ssl = False

"""

    # Set authentication
    if parsed_context.auth and parsed_context.auth != ():
        code += "# Set authentication\n"
        if len(parsed_context.auth) > 1:
            code += f"client.set_auth(\"{parsed_context.auth[0]}\", \"{parsed_context.auth[1]}\")\n\n"
        else:
            code += f"client.set_auth(\"{parsed_context.auth[0]}\", \"\")\n\n"

    # Set proxy
    if parsed_context.proxy:
        code += "# Set proxy\n"
        proxy_url = None
        if "http" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["http"]
        elif "https" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["https"]

        if proxy_url:
            code += f"client.set_proxy(\"{proxy_url}\")\n\n"

    # Set additional options
    if kwargs:
        code += "# Set additional options\n"
        for key, value in sorted(kwargs.items()):
            code += f"client.{key} = {value}\n"
        code += "\n"

    # Perform request
    method = parsed_context.method.upper()
    url = parsed_context.url

    code += "# Perform request\n"

    # Handle different HTTP methods with better formatting
    if method == "GET":
        code += f"""response = client.get(
        url="{url}",
        headers=headers
)

"""
    elif method == "POST":
        if parsed_context.data:
            code += f"""# Set data
data = '''{parsed_context.data}'''

response = client.post(
        url="{url}",
        data=data,
        headers=headers
)

"""
        else:
            code += f"""response = client.post(
        url="{url}",
        headers=headers
)

"""
    elif method == "PUT":
        if parsed_context.data:
            code += f"""# Set data
data = '''{parsed_context.data}'''

response = client.put(
        url="{url}",
        data=data,
        headers=headers
)

"""
        else:
            code += f"""response = client.put(
        url="{url}",
        headers=headers
)

"""
    elif method == "DELETE":
        code += f"""response = client.delete(
        url="{url}",
        headers=headers
)

"""
    elif method == "PATCH":
        if parsed_context.data:
            code += f"""# Set data
data = '''{parsed_context.data}'''

response = client.patch(
        url="{url}",
        data=data,
        headers=headers
)

"""
        else:
            code += f"""response = client.patch(
        url="{url}",
        headers=headers
)

"""
    elif method == "HEAD":
        code += f"""response = client.head(
        url="{url}",
        headers=headers
)

"""
    elif method == "OPTIONS":
        code += f"""response = client.options(
        url="{url}",
        headers=headers
)

"""
    else:
        # For any other method, use the request method
        if parsed_context.data:
            code += f"""# Set data
data = '''{parsed_context.data}'''

response = client.request(
        method="{method}",
        url="{url}",
        data=data,
        headers=headers
)

"""
        else:
            code += f"""response = client.request(
        method="{method}",
        url="{url}",
        headers=headers
)

"""

    # Print response information
    code += """# Print response information
print(f"Status Code: {response.status_code}")
print(f"Headers: {response.headers}")
print("Response Body:")
print(response.text)

"""

    # Close client
    code += """# Close client
client.close()
"""

    return code
