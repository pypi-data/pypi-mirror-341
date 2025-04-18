# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
from typing import Any

from ..common import ParsedContext


def generate_pycurl_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Generate Python pycurl code from a ParsedContext object.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments to pass to the pycurl call

    Returns:
        A string containing Python code that uses the pycurl library
    """
    # Import statement for pycurl
    import_statement = "import pycurl\nfrom io import BytesIO\nimport urllib.parse\nimport json\n\n"

    # Create the code
    code = _format_code(parsed_context, **kwargs)

    return import_statement + code


def _format_code(parsed_context: ParsedContext, **kwargs: Any) -> str:
    """Format the pycurl code.

    Args:
        parsed_context: The parsed curl command
        **kwargs: Additional keyword arguments

    Returns:
        The formatted pycurl code
    """
    # Use a multi-line string for better readability
    code = f"""# Initialize buffer and curl object
buffer = BytesIO()
c = pycurl.Curl()

# Set URL
c.setopt(pycurl.URL, "{parsed_context.url}")
"""

    # Set method
    if parsed_context.method.upper() != "GET":
        code += f"""# Set method
c.setopt(pycurl.CUSTOMREQUEST, "{parsed_context.method.upper()}")

"""

    # Set headers
    if parsed_context.headers:
        code += "# Set headers\nheaders = [\n"
        for key, value in sorted(parsed_context.headers.items()):
            code += f"    \"{key}: {value}\",\n"
        code += "]\nc.setopt(pycurl.HTTPHEADER, headers)\n\n"

    # Set cookies
    if parsed_context.cookies:
        code += "# Set cookies\n"
        if len(parsed_context.cookies) == 1:
            key, value = next(iter(parsed_context.cookies.items()))
            code += f"cookie_string = \"{key}={value}\"\n"
        else:
            code += "cookie_string = \"\"\n"
            for i, (key, value) in enumerate(sorted(parsed_context.cookies.items())):
                if i > 0:
                    code += f"cookie_string += \"; {key}={value}\"\n"
                else:
                    code += f"cookie_string = \"{key}={value}\"\n"
        code += "c.setopt(pycurl.COOKIE, cookie_string)\n\n"

    # Set data
    if parsed_context.data:
        # Check if data is JSON
        if _is_json(parsed_context.data):
            code += f"""# Set JSON data
data = '''{parsed_context.data}'''
c.setopt(pycurl.POSTFIELDS, data)

"""
        # Check if data is form data
        elif "=" in parsed_context.data and "&" in parsed_context.data:
            code += f"""# Set form data
data = '''{parsed_context.data}'''
c.setopt(pycurl.POSTFIELDS, data)

"""
        else:
            code += f"""# Set data
data = '''{parsed_context.data}'''
c.setopt(pycurl.POSTFIELDS, data)

"""

    # Set SSL verification
    if not parsed_context.verify:
        code += """# Disable SSL verification
c.setopt(pycurl.SSL_VERIFYPEER, 0)
c.setopt(pycurl.SSL_VERIFYHOST, 0)

"""

    # Set authentication
    if parsed_context.auth and parsed_context.auth != ():
        code += "# Set authentication\n"
        if len(parsed_context.auth) > 1:
            code += f"c.setopt(pycurl.USERPWD, \"{parsed_context.auth[0]}:{parsed_context.auth[1]}\")\n\n"
        else:
            code += f"c.setopt(pycurl.USERPWD, \"{parsed_context.auth[0]}:\")\n\n"

    # Set proxy
    if parsed_context.proxy:
        code += "# Set proxy\n"
        proxy_url = None
        if "http" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["http"]
        elif "https" in parsed_context.proxy:
            proxy_url = parsed_context.proxy["https"]

        if proxy_url:
            # Extract proxy details
            proxy_pattern = r"http://(?:(.+)@)?(.+)/"
            match = re.match(proxy_pattern, proxy_url)
            if match:
                proxy_auth, proxy_host = match.groups()
                code += f"c.setopt(pycurl.PROXY, \"{proxy_host}\")\n"
                if proxy_auth:
                    code += f"c.setopt(pycurl.PROXYUSERPWD, \"{proxy_auth}\")\n"
                code += "\n"

    # Set additional options
    if kwargs:
        code += "# Set additional options\n"
        for key, value in sorted(kwargs.items()):
            code += f"c.setopt(pycurl.{key.upper()}, {value})\n"
        code += "\n"

    # Add the rest of the code using multi-line strings for better readability
    code += """# Set write function
c.setopt(pycurl.WRITEFUNCTION, buffer.write)

# Perform request
c.perform()

# Get response info
response_code = c.getinfo(pycurl.RESPONSE_CODE)
content_type = c.getinfo(pycurl.CONTENT_TYPE)
total_time = c.getinfo(pycurl.TOTAL_TIME)

# Close curl object
c.close()

# Get response body
body = buffer.getvalue().decode('utf-8')

# Print response information
print(f"Response Code: {response_code}")
print(f"Content Type: {content_type}")
print(f"Total Time: {total_time} seconds")
print("Response Body:")
print(body)
"""

    return code


def _is_json(data: str) -> bool:
    """Check if a string is valid JSON.

    Args:
        data: The string to check

    Returns:
        True if the string is valid JSON, False otherwise
    """
    try:
        json.loads(data)
        return True
    except (ValueError, TypeError):
        return False
