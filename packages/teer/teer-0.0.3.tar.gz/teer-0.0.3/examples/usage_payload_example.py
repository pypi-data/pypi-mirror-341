"""
Example of creating a usage payload for the Teer ingest API.

This example demonstrates how to create a payload for the Teer ingest API
from an LLM provider response or from explicit token counts.
"""

from typing import Dict, Any, Optional


def create_usage_payload(
    provider: str,
    model: str,
    function_id: str,
    response: Optional[Any] = None,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Create a payload for the Teer ingest API.

    This function can be used in two ways:
    1. Pass a response object from an LLM provider (e.g., Anthropic) and it will extract the usage information
    2. Directly provide input_tokens and output_tokens if you already have them

    Args:
        provider: The LLM provider (e.g., "anthropic", "openai").
        model: The model name (e.g., "claude-3-haiku-20240307").
        function_id: An identifier for the function or endpoint using the LLM.
        response: Optional response object from the LLM provider (e.g., Anthropic message).
        input_tokens: Optional number of input tokens used (if not providing response).
        output_tokens: Optional number of output tokens generated (if not providing response).
        metadata: Optional additional metadata.

    Returns:
        A dictionary payload ready to be sent to the Teer ingest API.
    """
    # Initialize usage information
    usage_data = {}
    cache_info = None

    # Extract usage information from response if provided
    if response is not None:
        if provider == "anthropic":
            # Extract usage information from Anthropic response
            if hasattr(response, "usage"):
                # Extract standard token counts
                usage_data["input"] = getattr(response.usage, "input_tokens", 0)
                usage_data["output"] = getattr(response.usage, "output_tokens", 0)

                # Extract cache-related token information
                cache_read = getattr(response.usage, "cache_read_input_tokens", 0)
                cache_creation = getattr(
                    response.usage, "cache_creation_input_tokens", 0
                )

                # Create cache info if cache tokens are present
                if cache_read > 0 or cache_creation > 0:
                    cache_info = {
                        "anthropic": {
                            "cache_read_input_tokens": cache_read,
                            "cache_creation_input_tokens": cache_creation,
                        }
                    }
            else:
                print(f"No usage information found in {provider} response")
        else:
            # For other providers, implement their specific extraction logic here
            print(f"Usage extraction not implemented for provider: {provider}")
    else:
        # Use provided token counts if response is not available
        if input_tokens is not None and output_tokens is not None:
            usage_data["input"] = input_tokens
            usage_data["output"] = output_tokens
        else:
            raise ValueError(
                "Either response or input_tokens and output_tokens must be provided"
            )

    # Create the payload
    payload = {
        "provider": provider,
        "model": model,
        "function_id": function_id,
        "usage": usage_data,
    }

    # Add cache information if available
    if cache_info:
        payload["usage"]["cache"] = cache_info

    # Add metadata if provided
    if metadata:
        payload["metadata"] = metadata

    return payload


# Example 1: Creating a payload with explicit token counts
payload1 = create_usage_payload(
    provider="anthropic",
    model="claude-3-haiku-20240307",
    function_id="my-function",
    input_tokens=1000,
    output_tokens=2000,
    metadata={"user_id": "user123", "session_id": "session456"}
)

print("Example 1: Creating a payload with explicit token counts")
print(f"Payload: {payload1}")
print()

# Example 2: Creating a payload from an Anthropic response (simulated)
class MockAnthropicUsage:
    def __init__(self):
        self.input_tokens = 1500
        self.output_tokens = 2500
        self.cache_read_input_tokens = 500
        self.cache_creation_input_tokens = 1000

class MockAnthropicResponse:
    def __init__(self):
        self.usage = MockAnthropicUsage()

# Create a mock Anthropic response
anthropic_response = MockAnthropicResponse()

payload2 = create_usage_payload(
    provider="anthropic",
    model="claude-3-haiku-20240307",
    function_id="my-function",
    response=anthropic_response
)

print("Example 2: Creating a payload from an Anthropic response")
print(f"Payload: {payload2}")
