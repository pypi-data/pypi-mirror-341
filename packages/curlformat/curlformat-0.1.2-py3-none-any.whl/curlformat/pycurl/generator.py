# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from typing import Any, Dict, List

from ..common import ParsedContext, dict_to_pretty_string


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
    # Initialize buffer and curl object
    code = "# Initialize buffer and curl object\n"
    code += "buffer = BytesIO()\n"
    code += "c = pycurl.Curl()\n\n"
    
    # Set URL
    code += f"# Set URL\nc.setopt(pycurl.URL, \"{parsed_context.url}\")\n\n"
    
    # Set method
    if parsed_context.method.upper() != "GET":
        code += f"# Set method\nc.setopt(pycurl.CUSTOMREQUEST, \"{parsed_context.method.upper()}\")\n\n"
    
    # Set headers
    if parsed_context.headers:
        code += "# Set headers\nheaders = [\n"
        for key, value in parsed_context.headers.items():
            code += f"    \"{key}: {value}\",\n"
        code += "]\n"
        code += "c.setopt(pycurl.HTTPHEADER, headers)\n\n"
    
    # Set cookies
    if parsed_context.cookies:
        code += "# Set cookies\ncookie_string = \"\"\n"
        for key, value in parsed_context.cookies.items():
            code += f"cookie_string += \"{key}={value}; \"\n"
        code += "c.setopt(pycurl.COOKIE, cookie_string)\n\n"
    
    # Set data
    if parsed_context.data:
        # Check if data is JSON
        if _is_json(parsed_context.data):
            code += "# Set JSON data\n"
            code += f"data = '{parsed_context.data}'\n"
            code += "c.setopt(pycurl.POSTFIELDS, data)\n\n"
        # Check if data is form data
        elif "=" in parsed_context.data and "&" in parsed_context.data:
            code += "# Set form data\n"
            code += f"data = '{parsed_context.data}'\n"
            code += "c.setopt(pycurl.POSTFIELDS, data)\n\n"
        else:
            code += "# Set data\n"
            code += f"data = '{parsed_context.data}'\n"
            code += "c.setopt(pycurl.POSTFIELDS, data)\n\n"
    
    # Set SSL verification
    if not parsed_context.verify:
        code += "# Disable SSL verification\n"
        code += "c.setopt(pycurl.SSL_VERIFYPEER, 0)\n"
        code += "c.setopt(pycurl.SSL_VERIFYHOST, 0)\n\n"
    
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
        for key, value in kwargs.items():
            code += f"c.setopt(pycurl.{key.upper()}, {value})\n"
        code += "\n"
    
    # Set write function
    code += "# Set write function\n"
    code += "c.setopt(pycurl.WRITEFUNCTION, buffer.write)\n\n"
    
    # Perform request and get response
    code += "# Perform request\n"
    code += "c.perform()\n\n"
    
    # Get response info
    code += "# Get response info\n"
    code += "response_code = c.getinfo(pycurl.RESPONSE_CODE)\n"
    code += "content_type = c.getinfo(pycurl.CONTENT_TYPE)\n"
    code += "total_time = c.getinfo(pycurl.TOTAL_TIME)\n\n"
    
    # Close curl object
    code += "# Close curl object\n"
    code += "c.close()\n\n"
    
    # Get response body
    code += "# Get response body\n"
    code += "body = buffer.getvalue().decode('utf-8')\n\n"
    
    # Print response
    code += "# Print response\n"
    code += "print(f\"Response Code: {response_code}\")\n"
    code += "print(f\"Content Type: {content_type}\")\n"
    code += "print(f\"Total Time: {total_time} seconds\")\n"
    code += "print(\"Response Body:\")\n"
    code += "print(body)\n"
    
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
