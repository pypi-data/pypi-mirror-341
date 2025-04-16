
# ISend Python SDK

This is a Python SDK for sending email and event data using the TruSender API.

## Installation

You can install it via pip:

```bash
pip install isend-python-sdk
```

```python
from isend import ISend

client = ISend("your_api_key")
client.send_email("WelcomeTemplate", "user@example.com", {"name": "John"})
client.send_event("Signup", "user@example.com", {"plan": "Free"})
```