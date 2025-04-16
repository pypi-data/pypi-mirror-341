# AIIA SDK

The official SDK for integrating the AIIA protocol (Artificial Intelligence Interaction Agreement) into your AI systems.  
This library allows AI applications to log actions in a secure, auditable, and legally traceable way.

## What this SDK does

This SDK enables developers to integrate real-time action logging into their AI systems. It includes:

- A secure structure to log AI actions using a defined taxonomy of categorized actions (`aiia_actions_v1.0.json`)
- Cryptographic signature for each log to ensure integrity and traceability
- Built-in validation to match logged actions against the official dictionary and risk classification
- Automatic generation of timestamps and UUIDs for each entry
- Environment variable support for secure key management
- Flexible API endpoint configuration
- Error logging and silent failure handling for production safety

## Features

- Logs AI actions with associated metadata (timestamp, domain, identifiers)
- Digital signature for every action log using the client secret
- Validates actions against an extensible JSON dictionary
- Classifies actions by risk and sensitivity for audit
- Secure headers and payload structure for log submission
- Lightweight and easy to integrate into any Python-based AI application

## Installation

```bash
pip install aiia_sdk
```

## Usage Example

```python
from aiia_sdk import AIIA

ai = AIIA(
    api_key="your_api_key",
    client_secret="your_client_secret",
    ia_id="your_ia_id",
    endpoint="https://yourserver.com/receive_log"
)

# Log an action (e.g., sending an email)
ai.log_action("email.send", {
    "recipient": "user@example.com",
    "subject": "Welcome!"
})
```

## Logging Mechanism

When you call `log_action()`, the SDK will:

1. Load the official AIIA action dictionary and check if the action is allowed
2. Generate a unique log entry with timestamp, action, and optional metadata
3. Sign the payload using HMAC and the client secret
4. Send the log to the configured endpoint using a secure POST request

## Configuration

You can also use a `.env` file to store sensitive keys:

```
AIIA_API_KEY=your_api_key
AIIA_CLIENT_SECRET=your_client_secret
AIIA_IA_ID=your_ia_id
AIIA_ENDPOINT=https://yourserver.com/receive_log
```

Then instantiate without arguments:

```python
ai = AIIA()
```

## Documentation

Official documentation is currently under development and will be released soon.

## License

This SDK is released under the MIT License. See `LICENSE` for more information.