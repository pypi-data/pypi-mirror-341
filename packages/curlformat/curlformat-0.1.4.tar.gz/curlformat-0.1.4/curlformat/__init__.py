from .common import parse_context
from .requests import parse

# Import httpx parser if available
try:
    from .httpx import parse as parse_httpx, parse_async as parse_httpx_async
    httpx_available = True
except ImportError:
    httpx_available = False

# Import aiohttp parser if available
try:
    from .aiohttp import parse as parse_aiohttp
    aiohttp_available = True
except ImportError:
    aiohttp_available = False

# Import pycurl parser if available
try:
    from .pycurl import parse as parse_pycurl
    pycurl_available = True
except ImportError:
    pycurl_available = False

# Import pyhttpx parser if available
try:
    from .pyhttpx import parse as parse_pyhttpx
    pyhttpx_available = True
except ImportError:
    pyhttpx_available = False

# Import curl_cffi parser if available
try:
    from .curl_cffi import parse as parse_curl_cffi, parse_async as parse_curl_cffi_async
    curl_cffi_available = True
except ImportError:
    curl_cffi_available = False

# Define __all__ based on available modules
__all__ = ['parse', 'parse_context']

if httpx_available:
    __all__.extend(['parse_httpx', 'parse_httpx_async'])

if aiohttp_available:
    __all__.append('parse_aiohttp')

if pycurl_available:
    __all__.append('parse_pycurl')

if pyhttpx_available:
    __all__.append('parse_pyhttpx')

if curl_cffi_available:
    __all__.extend(['parse_curl_cffi', 'parse_curl_cffi_async'])
