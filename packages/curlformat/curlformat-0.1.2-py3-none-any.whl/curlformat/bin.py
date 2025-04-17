# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import sys

import pyperclip
from .requests import parse as parse_requests

# Import httpx parser if available
try:
    from .httpx import parse as parse_httpx, parse_async as parse_httpx_async
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

# Import aiohttp parser if available
try:
    from .aiohttp import parse as parse_aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

# Import pycurl parser if available
try:
    from .pycurl import parse as parse_pycurl
    PYCURL_AVAILABLE = True
except ImportError:
    PYCURL_AVAILABLE = False

# Import pyhttpx parser if available
try:
    from .pyhttpx import parse as parse_pyhttpx
    PYHTTPX_AVAILABLE = True
except ImportError:
    PYHTTPX_AVAILABLE = False

# Import curl_cffi parser if available
try:
    from .curl_cffi import parse as parse_curl_cffi, parse_async as parse_curl_cffi_async
    CURL_CFFI_AVAILABLE = True
except ImportError:
    CURL_CFFI_AVAILABLE = False


def display_operations_list():
    """Display a formatted list of available operations."""
    print("\nAvailable operations:")
    print("-------------------")
    print("1. requests - Default HTTP library")

    if HTTPX_AVAILABLE:
        print("2. httpx    - Modern HTTP client with sync and async support")
        print("             Use --httpx --async for async mode")
    else:
        print("2. httpx    - [Not available] Install the httpx package to enable")

    if AIOHTTP_AVAILABLE:
        print("3. aiohttp  - Async HTTP client/server framework")
    else:
        print("3. aiohttp  - [Not available] Install the aiohttp package to enable")

    if PYCURL_AVAILABLE:
        print("4. pycurl   - Python interface to libcurl")
    else:
        print("4. pycurl   - [Not available] Install the pycurl package to enable")

    if PYHTTPX_AVAILABLE:
        print("5. pyhttpx  - Python HTTP client library")
    else:
        print("5. pyhttpx  - [Not available] Install the pyhttpx package to enable")

    if CURL_CFFI_AVAILABLE:
        print("6. curl_cffi - Python binding for curl-impersonate")
        print("             Use --curl-cffi --async for async mode")
    else:
        print("6. curl_cffi - [Not available] Install the curl_cffi package to enable")

    print("\nUsage examples:")
    print("  curlformat 'curl -X GET \"https://api.example.com\"'")
    print("  curlformat --httpx 'curl -X GET \"https://api.example.com\"'")
    print("  curlformat --httpx --async 'curl -X GET \"https://api.example.com\"'")
    print("  cat curl_command.txt | curlformat --aiohttp")
    print("\nIf no curl command is provided, curlformat will try to read from clipboard.")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Convert curl commands to Python code for various HTTP libraries')
    parser.add_argument('--httpx', action='store_true', help='Generate httpx code instead of requests')
    parser.add_argument('--aiohttp', action='store_true', help='Generate aiohttp code')
    parser.add_argument('--pycurl', action='store_true', help='Generate pycurl code')
    parser.add_argument('--pyhttpx', action='store_true', help='Generate pyhttpx code')
    parser.add_argument('--curl-cffi', action='store_true', help='Generate curl_cffi code')
    parser.add_argument('--async', dest='async_mode', action='store_true', help='Generate async code (works with httpx and curl_cffi)')
    parser.add_argument('--list', action='store_true', help='Display a list of available operations')
    parser.add_argument('curl_command', nargs='?', help='The curl command to parse')

    # Parse arguments
    args = parser.parse_args()

    # Determine which parser to use
    # Check if multiple libraries are specified
    libraries = [args.httpx, args.aiohttp, args.pycurl, args.pyhttpx, args.curl_cffi].count(True)
    if libraries > 1:
        print("Error: Cannot use multiple library flags together. Please choose one.")
        sys.exit(1)

    if args.httpx:
        if not HTTPX_AVAILABLE:
            print("Error: httpx support is not available. Please install the httpx package.")
            sys.exit(1)
        if args.async_mode:
            parse_func = parse_httpx_async
        else:
            parse_func = parse_httpx
    elif args.aiohttp:
        if not AIOHTTP_AVAILABLE:
            print("Error: aiohttp support is not available. Please install the aiohttp package.")
            sys.exit(1)
        if args.async_mode:
            print("Warning: aiohttp is already async. Ignoring --async flag.")
        parse_func = parse_aiohttp
    elif args.pycurl:
        if not PYCURL_AVAILABLE:
            print("Error: pycurl support is not available. Please install the pycurl package.")
            sys.exit(1)
        if args.async_mode:
            print("Warning: pycurl does not support async mode. Ignoring --async flag.")
        parse_func = parse_pycurl
    elif args.pyhttpx:
        if not PYHTTPX_AVAILABLE:
            print("Error: pyhttpx support is not available. Please install the pyhttpx package.")
            sys.exit(1)
        if args.async_mode:
            print("Warning: pyhttpx does not support async mode. Ignoring --async flag.")
        parse_func = parse_pyhttpx
    elif args.curl_cffi:
        if not CURL_CFFI_AVAILABLE:
            print("Error: curl_cffi support is not available. Please install the curl_cffi package.")
            sys.exit(1)
        if args.async_mode:
            parse_func = parse_curl_cffi_async
        else:
            parse_func = parse_curl_cffi
    else:
        if args.async_mode:
            print("Warning: Async mode is only available with httpx and curl_cffi. Ignoring --async flag.")
        parse_func = parse_requests

    # Check if user wants to display the operations list
    if args.list:
        display_operations_list()
        return

    # Get the curl command from arguments, clipboard, or stdin
    if sys.stdin.isatty():
        if args.curl_command:
            # If an argument is passed
            curl_command = args.curl_command
        else:
            # If no argument and no library specified, show operations list
            if not any([args.httpx, args.aiohttp, args.pycurl, args.pyhttpx, args.curl_cffi]):
                display_operations_list()
                return
            # Otherwise pull from clipboard
            curl_command = pyperclip.paste()
    else:
        curl_command = sys.stdin.read()

    try:
        # Parse the curl command
        result = parse_func(curl_command)
        print("\n" + result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
