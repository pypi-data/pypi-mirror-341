# Teer Python SDK

[![PyPI - Version](https://img.shields.io/pypi/v/teer.svg)](https://pypi.org/project/teer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/teer.svg)](https://pypi.org/project/teer)

The official Python SDK for [Teer](https://teer.ai), a platform for tracking and analyzing LLM usage across multiple providers including Anthropic, OpenAI, and Google.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Usage Reports](#usage-reports)
- [Examples](#examples)
- [Documentation](#documentation)
- [License](#license)

## Installation

```console
pip install teer
```

## Usage

### Initializing the Client

```python
from teer import TeerClient

# Initialize with your API key
client = TeerClient("YOUR_API_KEY")

# Or initialize with a custom base URL (e.g., for development or enterprise deployments)
client = TeerClient(
    api_key="YOUR_API_KEY",
    base_url="https://dev-track.teer.ai"
)
```

### Sending Basic Usage Data

```python
# Send basic usage data
client.ingest.send({
    # Required: Specify the LLM provider
    "provider": "anthropic",

    # Required: Specify the model name
    "model": "claude-3-haiku-20240307",

    # Optional: A unique identifier for the function or endpoint using the LLM
    "function_id": "summarize-article",

    # Required: Token usage information
    "usage": {
        # Number of input tokens
        "input": 1000,
        # Number of output tokens
        "output": 2000
    }
})
```

## Usage Reports

Teer supports detailed usage reports for different LLM providers. Here are some examples of more advanced usage reports:

### Usage Report with Cache Information

```python
client.ingest.send({
    "provider": "anthropic",
    "model": "claude-3-opus-20240229",
    "function_id": "legal-document-analysis",
    "usage": {
        "input": 2000,
        "output": 3000,
        # Anthropic-specific cache information
        "cache": {
            "anthropic": {
                # Tokens used to create the cache
                "cache_creation_input_tokens": 1500,
                # Tokens read from the cache
                "cache_read_input_tokens": 500
            }
        }
    }
})
```

### Usage Report with User Attribution

```python
client.ingest.send({
    "provider": "openai",
    "model": "gpt-4o-mini-2024-07-18",
    "function_id": "generate-content",
    "usage": {
        "input": 500,
        "output": 1500
    },
    # Metadata for user attribution and analytics
    "metadata": {
        # User identification
        "user_id": "user-123456",
        "organization_id": "org-abcdef",

        # Session information
        "session_id": "session-xyz789"
    }
})
```

### Usage Report Without Function ID

```python
client.ingest.send({
    # Required: Specify the LLM provider
    "provider": "google",

    # Required: Specify the model name
    "model": "gemini-2.0-flash-001",

    # function_id is optional and can be omitted

    # Required: Token usage information
    "usage": {
        "input": 400,
        "output": 1200
    }
})
```

For a complete reference of all supported fields in usage reports, see the [Usage Reports documentation](./docs/usage_reports.md).

## Examples

Check out the [examples](./examples) directory for more usage examples:

- [Basic Usage](./examples/basic_usage.py): Simple example of using the Teer client
- [Custom Base URL](./examples/custom_base_url.py): Example of initializing the Teer client with a custom base URL
- [Comprehensive Usage Reports](./examples/comprehensive_usage_reports.py): Detailed examples of various usage report scenarios
- [Usage Payload Example](./examples/usage_payload_example.py): Example of creating a payload for the Teer ingest API

## Documentation

Detailed documentation is available in the [docs](./docs) directory:

- [Usage Reports](./docs/usage_reports.md): Detailed information about the structure and fields of usage reports

## License

`teer` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
