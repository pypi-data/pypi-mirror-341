# curlformat

A Python package to convert curl commands to Python HTTP client code.

## Features

- Convert curl commands to Python code for various HTTP libraries:
  - requests (default)
  - httpx (with sync and async support)
  - aiohttp
  - pycurl
  - pyhttpx
  - curl_cffi (with sync and async support, random browser impersonation)
  - requests_go (with TLS configuration support)
- Parse curl commands from command line, clipboard, or stdin
- Support for headers, cookies, data, and more

## Installation

```bash
pip install curlformat
```

## Usage

### Command Line

```bash
# Basic usage (converts to requests)
curlformat 'curl -X GET "https://api.example.com"'

# Convert to httpx
curlformat --httpx 'curl -X GET "https://api.example.com"'

# Convert to async httpx
curlformat --httpx --async 'curl -X GET "https://api.example.com"'

# Convert to aiohttp
curlformat --aiohttp 'curl -X GET "https://api.example.com"'

# Convert to curl_cffi with random browser impersonation
curlformat --curl-cffi 'curl -X GET "https://api.example.com"'

# Convert to requests_go with TLS configuration
curlformat --requests-go 'curl -X GET "https://api.example.com"'

# Read from clipboard if no curl command is provided
curlformat --httpx

# Read from stdin
cat curl_command.txt | curlformat --pycurl
```

### Python API

```python
from curlformat import parse

# Convert curl command to requests code
python_code = parse('curl -X GET "https://api.example.com"')
print(python_code)

# If httpx is installed
from curlformat import parse_httpx, parse_httpx_async

# Convert to httpx code
httpx_code = parse_httpx('curl -X GET "https://api.example.com"')
print(httpx_code)

# Convert to async httpx code
httpx_async_code = parse_httpx_async('curl -X GET "https://api.example.com"')
print(httpx_async_code)

# If curl_cffi is installed
from curlformat import parse_curl_cffi, parse_curl_cffi_async

# Convert to curl_cffi code with random browser impersonation
curl_cffi_code = parse_curl_cffi('curl -X GET "https://api.example.com"')
print(curl_cffi_code)

# Convert to async curl_cffi code with random browser impersonation
curl_cffi_async_code = parse_curl_cffi_async('curl -X GET "https://api.example.com"')
print(curl_cffi_async_code)

# If requests_go is installed
from curlformat import parse_requests_go

# Convert to requests_go code with TLS configuration
requests_go_code = parse_requests_go('curl -X GET "https://api.example.com"')
print(requests_go_code)
```

## Optional Dependencies

The package has the following optional dependencies:

- `httpx`: For httpx support
- `aiohttp`: For aiohttp support
- `pycurl`: For pycurl support
- `pyhttpx`: For pyhttpx support
- `curl_cffi`: For curl_cffi support with random browser impersonation
- `requests_go`: For requests_go support with TLS configuration

You can install all optional dependencies with:

```bash
pip install curlformat[all]
```

Or install specific dependencies:

```bash
pip install curlformat[httpx,aiohttp]
```

## License

MIT
