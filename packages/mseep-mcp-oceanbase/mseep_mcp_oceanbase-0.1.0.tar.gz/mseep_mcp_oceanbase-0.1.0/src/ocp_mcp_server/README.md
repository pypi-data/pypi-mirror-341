# mcp-oceanbase

MCP Server for OCP (OceanBase Cloud Platform).

English | [简体中文](README_CN.md)

## Features

This repository contains MCP Servers as following:

| MCP Server           | Description      | 
|----------------------|------------------|
| OCP MCP Server | A Model Context Protocol (MCP) server that enables secure interaction with OCP. |

## Usage

To use with the MCP Client, it is necessary to utilize a client that supports Prompt, such as Claude Desktop. Before entering a request, you need to manually select the desired Prompt and then input your request.

![](assets/ocp_claude.jpg)

Claude Desktop config  example:

```json
 "ocp": {
            "command": "{python or uv}",
            "args": [
              "{Your path}/mcp-oceanbase/src/ocp_mcp_server/server.py"
            ],
            "env": {
              "AK": "******",
              "SK": "******",
              "ADDRESS":"ip:port"
            }
          }
```

## Community

Don’t hesitate to ask!

Contact the developers and community at [https://ask.oceanbase.com](https://ask.oceanbase.com) if you need any help.

[Open an issue](https://github.com/oceanbase/mcp-oceanbase/issues) if you found a bug.

## Licensing

See [LICENSE](LICENSE) for more information.