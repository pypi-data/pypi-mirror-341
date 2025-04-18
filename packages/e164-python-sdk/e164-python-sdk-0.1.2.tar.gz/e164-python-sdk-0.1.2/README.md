# E164 Python SDK

A Python library for handling E.164 formatted phone numbers. This library allows you to validate and retrieve metadata about phone numbers using the e164.com API.

## Installation

```bash
pip install e164-python-sdk
```

## Usage

Here's a quickstart guide to using the library:

```python
from e164_python_sdk.e164 import E164

# Initialize the E164 client
client = E164()

# Lookup a phone number
try:
    response = client.lookup("+441133910781")
    print(response.to_dict())  # Print the response as a dictionary
except ValueError as e:
    print(f"Error: {e}")
```

## Features

- Validate E.164 formatted phone numbers.
- Retrieve metadata such as country code, operator, and phone number type.
- Easy-to-use Python interface.

For more details, refer to the documentation or explore the source code.
