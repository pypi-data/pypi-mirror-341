import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath("src"))

# Import the TeerClient
from teer import TeerClient

# Create a client with a dummy API key
client = TeerClient(api_key="test_api_key")

# Print the client details
print(f"Client initialized with API key: {client.api_key}")
print(f"Base URL: {client.base_url}")
print(f"API base: {client.api_base}")

# Verify that the ingest resource is available
print(f"Ingest resource: {client.ingest}")

print("Test completed successfully!")
