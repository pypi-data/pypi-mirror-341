# Workwize MCP Server

An MCP server implementation for the Workwize Public API.

## Features

- Access to Workwize Public API through MCP tools
- Secure API token handling
- Easy to extend with new tools

## Setup

1. Install the package:
```bash
pip install .
```

2. Create a `.env` file with your Workwize API token:
```bash
WORKWIZE_API_TOKEN=your_token_here
```

## Usage

Start the server:
```bash
python wize-mcp
```

## Local Installation with Claude for Desktop

To use this MCP server locally with Claude for Desktop:

1. Make sure you have Claude for Desktop installed and updated to the latest version.

2. Configure Claude for Desktop by editing the configuration file:

   **On MacOS**:
   ```bash
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

   **On Windows**:
   ```powershell
   code $env:AppData\Claude\claude_desktop_config.json
   ```

   Create the file if it doesn't exist.

3. Add the Wize MCP server to your configuration:

   ```json
   {
       "mcpServers": {
           "workwize": {
               "command": "uv",
               "args": [
                   "--directory",
                   "/path/to/wize-mcp",
                   "run",
                   "wize-mcp"
               ],
               "env": {
                   "WORKWIZE_API_TOKEN": "your_token_here"
               }
           }
       }
   }
   ```

4. Restart Claude for Desktop to load the configuration.

5. Verify the MCP server is working by looking for the hammer icon in the Claude interface.

## Adding New Tools

1. Create a new tool class in `src/wize-mcp/tools/`
2. Add the tool to the `_get_tools()` method in `src/wize-mcp/wize-mcp.py`
3. Update the API client in `src/wize-mcp/api/client.py` if needed

## License

MIT
