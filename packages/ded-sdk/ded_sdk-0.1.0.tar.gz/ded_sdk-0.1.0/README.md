# ded_sdk

**ded_sdk** is a Python SDK for detecting disposable email addresses using the [Disposable Email Detector API](https://ded.gossorg.in). It provides a simple interface to validate email addresses and determine if they are disposable.

## Features

- Validate email addresses for disposability.
- Retrieve detailed information about the email domain.
- Easy integration with Python applications.

## Installation

Install the SDK using pip:

```bash
pip install ded_sdk
```


## Usage

First, import the `DisposableEmailClient` and initialize it with your API key:

```python
from ded_sdk import DisposableEmailClient

api_key = "your-api-key"
client = DisposableEmailClient(api_key)
```


To validate an email address:

```python
email = "example@tempmail.com"
result = client.validate(email)

if result["disposable"]:
    print(f"{email} is disposable.")
else:
    print(f"{email} is not disposable.")
```


The `validate` method returns a dictionary with the following keys:

- `disposable`: Boolean indicating if the email is disposable.
- `domain`: The domain of the email address.
- `source`: Source of the information (e.g., "crawled").
- `confidence`: Confidence score between 0 and 1.

## API Reference

### `DisposableEmailClient(api_key: str, base_url: str = "https://ded.gossorg.in/v1")`

Initializes the client with your API key.

- `api_key`: Your API key for authentication.
- `base_url`: Base URL of the API (default is `https://ded.gossorg.in/v1`).

### `validate(email: str) -> dict`

Validates the provided email address.

- `email`: The email address to validate.

Returns a dictionary with the validation result.

## License

This project is licensed under the MIT License.

