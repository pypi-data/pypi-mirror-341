"""
Test script to verify that the package can be imported as expected.
"""

# Import the TeerClient class
from teer import TeerClient

# Create a client instance
client = TeerClient(api_key="test_api_key")

# Print the client details
print(f"Client initialized with API key: {client.api_key}")
print(f"Base URL: {client.base_url}")
print(f"API base: {client.api_base}")

# Verify that the ingest resource is available
print(f"Ingest resource: {client.ingest}")

print("Import test completed successfully!")
