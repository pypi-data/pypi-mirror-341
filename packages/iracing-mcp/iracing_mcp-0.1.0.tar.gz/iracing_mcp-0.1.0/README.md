# iRacing MCP

iRacing MCP is a Python-based project that integrates iRacing with the Model Context Protocol (MCP). It provides tools and resources to interact with iRacing data and build custom applications.

## Features

- Retrieve iRacing profile statistics.
- More coming soon

## Getting Started

### Prerequisites

- uv - [Install here](https://docs.astral.sh/uv/getting-started/installation/)
- iRacing account with legacy authentication (required) - Disable it here: https://oauth.iracing.com/accountmanagement/security

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/musantro/iracing-mcp.git
   cd iracing-mcp
   ```

2. Create environment with dependencies:

   ```bash
   uv sync
   ```

3. Set up environment variables for iRacing credentials:
   ```bash
   export IRACING_USERNAME="your_username"
   export IRACING_PASSWORD="your_password"
   ```

## Usage

### Running the Server Standalone

To start the MCP server, run:

```bash
uv run server
```

### Running the Server on VSCode

Add this to your settings.json (in `mcp.servers`):

```json
"iracing": {
    "command": "path/to/your/uv",
    "args": [
        "--directory",
        "path/to/your/iracing-mcp",
        "run",
        "server"
    ],
    "env": {
        "IRACING_USERNAME": "your-username",
        "IRACING_PASSWORD": "your password"
    }
}
```

## Development

### Linting and Formatting

Use the following commands to lint and format the code:

```bash
make
```

## Contributing

We welcome contributions! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Push your branch.
4. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
