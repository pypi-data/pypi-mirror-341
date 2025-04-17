"""
Basic usage example for the Teer Python SDK.

This example demonstrates how to use the Teer client to send usage data.
"""

from teer import TeerClient

# Initialize the client with your API key
client = TeerClient("YOUR_API_KEY")

# Send usage data
response = client.ingest.send({
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "function_id": "my-function",
    "usage": {
        "input": 1000,
        "output": 2000
    }
})

print(f"Response: {response}")
