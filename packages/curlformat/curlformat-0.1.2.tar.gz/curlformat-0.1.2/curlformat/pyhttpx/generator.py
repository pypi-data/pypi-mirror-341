# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, List

from ..common import ParsedContext, dict_to_pretty_string


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
    # Initialize client
    code = "# Initialize client\n"
    code += "client = pyhttpx.HttpClient()\n\n"
    
    # Set headers
    if parsed_context.headers:
        code += "# Set headers\n"
        code += "headers = {\n"
        for key, value in parsed_context.headers.items():
            code += f"    \"{key}\": \"{value}\",\n"
        code += "}\n\n"
    else:
        code += "# No headers specified\n"
        code += "headers = {}\n\n"
    
    # Set cookies
    if parsed_context.cookies:
        code += "# Set cookies\n"
        code += "cookies = {\n"
        for key, value in parsed_context.cookies.items():
            code += f"    \"{key}\": \"{value}\",\n"
        code += "}\n\n"
        code += "# Add cookies to client\n"
        code += "for key, value in cookies.items():\n"
        code += "    client.add_cookie(key, value)\n\n"
    
    # Set SSL verification
    if not parsed_context.verify:
        code += "# Disable SSL verification\n"
        code += "client.verify_ssl = False\n\n"
    
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
        for key, value in kwargs.items():
            code += f"client.{key} = {value}\n"
        code += "\n"
    
    # Perform request
    method = parsed_context.method.upper()
    url = parsed_context.url
    
    code += "# Perform request\n"
    
    # Handle different HTTP methods
    if method == "GET":
        code += f"response = client.get(\"{url}\", headers=headers)\n\n"
    elif method == "POST":
        if parsed_context.data:
            code += "# Set data\n"
            code += f"data = '{parsed_context.data}'\n"
            code += f"response = client.post(\"{url}\", data=data, headers=headers)\n\n"
        else:
            code += f"response = client.post(\"{url}\", headers=headers)\n\n"
    elif method == "PUT":
        if parsed_context.data:
            code += "# Set data\n"
            code += f"data = '{parsed_context.data}'\n"
            code += f"response = client.put(\"{url}\", data=data, headers=headers)\n\n"
        else:
            code += f"response = client.put(\"{url}\", headers=headers)\n\n"
    elif method == "DELETE":
        code += f"response = client.delete(\"{url}\", headers=headers)\n\n"
    elif method == "PATCH":
        if parsed_context.data:
            code += "# Set data\n"
            code += f"data = '{parsed_context.data}'\n"
            code += f"response = client.patch(\"{url}\", data=data, headers=headers)\n\n"
        else:
            code += f"response = client.patch(\"{url}\", headers=headers)\n\n"
    elif method == "HEAD":
        code += f"response = client.head(\"{url}\", headers=headers)\n\n"
    elif method == "OPTIONS":
        code += f"response = client.options(\"{url}\", headers=headers)\n\n"
    else:
        # For any other method, use the request method
        if parsed_context.data:
            code += "# Set data\n"
            code += f"data = '{parsed_context.data}'\n"
            code += f"response = client.request(\"{method}\", \"{url}\", data=data, headers=headers)\n\n"
        else:
            code += f"response = client.request(\"{method}\", \"{url}\", headers=headers)\n\n"
    
    # Print response
    code += "# Print response\n"
    code += "print(f\"Status Code: {response.status_code}\")\n"
    code += "print(f\"Headers: {response.headers}\")\n"
    code += "print(\"Response Body:\")\n"
    code += "print(response.text)\n\n"
    
    # Close client
    code += "# Close client\n"
    code += "client.close()\n"
    
    return code
