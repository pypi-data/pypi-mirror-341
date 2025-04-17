# A2A SDK

A2A SDK is a framework for building AI agents and applications. It provides core functionality for creating, managing, and communicating with AI agents.

## Features

- Type-safe agent communication protocol
- Built-in client and server implementations
- Extensible agent framework
- Support for multiple agent types and hosting environments

## Installation

```bash
pip install rubi_sdk
```

## Quick Start

### Creating a Server

```python
from rubi_sdk.server import A2AServer
from rubi_sdk.types import Task

server = A2AServer()
server.start()
```

### Creating a Client

```python
from rubi_sdk.client import A2AClient

client = A2AClient()
response = await client.send_task({"prompt": "Hello, world!"})
```

## Project Structure

The SDK is organized into the following main components:

- `rubi_sdk.types` - Core type definitions
- `rubi_sdk.client` - Client implementation
- `rubi_sdk.server` - Server implementation
- `rubi_sdk.utils` - Utility functions and classes

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file. 