# ✅ Official Alpha Vantage MCP Server

[![smithery badge](https://smithery.ai/badge/@calvernaz/alphavantage)](https://smithery.ai/server/@calvernaz/alphavantage)

A MCP server for the stock market data API, Alphavantage API. 

## Configuration

### Getting an API Key
1. Sign up for a [Free Alphavantage API key](https://www.alphavantage.co/support/#api-key)
2. Add the API key to your environment variables as `ALPHAVANTAGE_API_KEY`


## Clone the project

```bash
git clone https://github.com/calvernaz/alphavantage.git
```

### Usage with Claude Desktop
Add this to your `claude_desktop_config.json`:

**NOTE** Make sure you replace the `<DIRECTORY-OF-CLONED-PROJECT>` with the directory of the cloned project.

```
{
  "mcpServers": {
    "alphavantage": {
      "command": "uv",
      "args": [
        "--directory",
        "<DIRECTORY-OF-CLONED-PROJECT>/alphavantage",
        "run",
        "alphavantage"
      ],
      "env": {
        "ALPHAVANTAGE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

## 🤝 Contributing

We welcome contributions from the community! To get started, check out our [contribution](CONTRIBUTING.md) guide for setup instructions, 
development tips, and guidelines.