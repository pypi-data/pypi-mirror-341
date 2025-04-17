# Teer Python SDK

[![PyPI - Version](https://img.shields.io/pypi/v/teer.svg)](https://pypi.org/project/teer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/teer.svg)](https://pypi.org/project/teer)

The official Python SDK for [Teer](https://teer.ai), a platform for tracking and analyzing LLM usage.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

## Installation

```console
pip install teer
```

## Usage

```python
from teer import TeerClient

# Initialize with your API key
client = TeerClient("YOUR_API_KEY")

# Send usage data
client.ingest.send({
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "function_id": "my-function",
    "usage": {
        "input": 1000,
        "output": 2000
    }
})
```

## Examples

Check out the [examples](./examples) directory for more usage examples:

- [Basic Usage](./examples/basic_usage.py): Simple example of using the Teer client
- [Usage Payload Example](./examples/usage_payload_example.py): Example of creating a payload for the Teer ingest API

## License

`teer` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
