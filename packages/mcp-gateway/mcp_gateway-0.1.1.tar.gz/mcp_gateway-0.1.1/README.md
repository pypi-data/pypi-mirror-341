# MCP Gateway

![Hugging Face Token Masking Example](https://raw.githubusercontent.com/lasso-security/mcp-gateway/main/docs/MCP_Flow.png)

MCP Gateway is an advanced intermediary solution for Model Context Protocol (MCP) servers that centralizes and enhances your AI infrastructure.

## How It Works
Your agent interacts directly with our MCP Gateway, which functions as a central router and management system. Each underlying MCP is individually wrapped and managed.

### Key Features

#### Agnostic Guardrails
* Applies configurable security filters to both requests and responses.
* Prevents sensitive data exposure before information reaches your agent.
* Works consistently across all connected MCPs regardless of their native capabilities.

#### Unified Visibility
* Provides comprehensive dashboard for all your MCPs in a single interface.
* Includes intelligent risk assessment with MCP risk scoring.
* Delivers real-time status monitoring and performance metrics.

#### Advanced Tracking
* Maintains detailed logs of all requests and responses for each guardrail.
* Offers cost evaluation tools for MCPs requiring paid tokens.
* Provides usage analytics and pattern identification for optimization.
* Sanitizes sensitive information before forwarding requests to other MCPs.

## Overview

MCP Gateway acts as an intermediary between LLMs and other MCP servers. It:

1. Reads server configurations from a `mcp.json` file located in your root directory.
2. Manages the lifecycle of configured MCP servers.
3. Intercepts requests and responses to sanitize sensitive information.
4. Provides a unified interface for discovering and interacting with all proxied MCPs.

## Installation
Install the mcp-proxy package:
```bash
pip install mcp-proxy
```

Install the mcp-proxy package with presidio guardrail:
```bash
pip install mcp-proxy[presidio]
```

## Run
This is an example of how to add to your mcp.json in cursor:
```json
{
  "mcpServers": {
      "mcp-gateway": {
          "command": "mcp-gateway",
          "args": [
              "--mcp-json-path",
              "~/.cursor/mcp.json",
              "--enable-guardrails",
              "basic",
              "--enable-guardrails",
              "presidio"
          ],
          "servers": {
              "filesystem": {
                  "command": "npx",
                  "args": [
                      "-y",
                      "@modelcontextprotocol/server-filesystem",
                      "."
                  ]
              }
          }
      }
  }
}
```

This example gives you the basic and presidio guardrails for token and PII masking for filesystem MCP.
You can add more MCPs that will be under the Gateway by putting the MCP server configuration under the "servers" key.

## Usage

Start the MCP Gateway server with python_env config on this repository root:

```bash
mcp-gateway --enable-guardrails basic --enable-guardrails presidio
```

You can also debug the server using:
```bash
LOGLEVEL=DEBUG mcp-gateway --mcp-json-path ~/.cursor/mcp.json --enable-guardrails basic --enable-guardrails presidio
```

## Features

- **Tool: `get_metadata`** - Provides information about all available proxied MCPs to help LLMs choose appropriate tools and resources
- **Tool: `run_tool`** - Executes capabilities from any proxied MCP after sanitizing the request and response

## Use Cases

### Masking Sensitive Information

MCP Gateway can mask sensitive information like tokens and credentials:

1. Create a file with sensitive information:
   ```bash
   echo 'HF_TOKEN = "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"' > tokens.txt
   ```

2. When an agent requests to read this file through MCP Gateway:
   ```
   Use your mcp-gateway tools to read the ${pwd}/tokens.txt and return the HF_TOKEN
   ```
   “Recommend with sonnet”


3. MCP Gateway will automatically mask the sensitive token in the response, preventing exposure of credentials while still providing the needed functionality.

### Example of Masked Sensitive Information

The image below shows how MCP Gateway automatically masks a Hugging Face token in the response:

![Hugging Face Token Masking Example](https://raw.githubusercontent.com/lasso-security/mcp-gateway/main/docs/hf_example.png)

## Using Lasso Guardrails

To use Lasso Security's advanced AI safety guardrails, update your `mcp.json` configuration as follows:

1. Replace the existing guardrails with the "lasso" guardrail.
2. Add the `LASSO_API_KEY` environment variable in the "env" section.

Here's how to configure it:

```json
{
  "mcpServers": {
      "mcp-gateway": {
          "command": "mcp-gateway",
          "args": [
              "--mcp-json-path",
              "~/.cursor/mcp.json",
              "--enable-guardrails",
              "lasso"
          ],
          "env": {
              "LASSO_API_KEY": "<lasso_token>"
          },
          "servers": {
              "filesystem": {
                  "command": "npx",
                  "args": [
                      "-y",
                      "@modelcontextprotocol/server-filesystem",
                      "."
                  ]
              }
          }
      }
  }
}
```

You will need to:

1. **Obtain a Lasso API key** by signing up at [Lasso Security](https://www.lasso.security/).
2. **Replace `<lasso_token>` with your actual Lasso API key**.

When running with Lasso guardrails, you can also use:

```bash
mcp-gateway --enable-guardrails lasso
```
With Lasso you get:

🔍 Full visibility into MCP interactions with an Always-on monitoring.

🛡️ Mitigate GenAI-specific threats like prompt injection and sensitive data leakage in real-time with built-in protection that prioritizes security from deployment.

✨ Use flexible, natural language to craft security policies tailored to your business's unique needs.

⚡ Fast and easy installation for any deployment style. Monitor data flow to and from MCP in minutes with an intuitive, user-friendly dashboard.

Lasso Security's guardrails provide advanced protection against:
- Prompt injections and jailbreak attempts
- Harmful content detection
- Data leak prevention
- Custom policy enforcement

The Lasso guardrail checks content through Lasso's API for security violations before processing requests and responses.

Read more in [Lasso Security](https://www.lasso.security/).

## License

MIT

