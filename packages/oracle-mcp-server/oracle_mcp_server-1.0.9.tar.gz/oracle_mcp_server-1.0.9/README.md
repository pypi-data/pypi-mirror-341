# oracle-mcp-server
Model Context Protocol server to access oracle, supporting Oracle 11g and above.


## Quickstart

add this to your cursor `mcp.json` config files:

```json
{
  "mcpServers": {
    "oracle-mcp-server": {
      "command": "uvx",
      "args": [
        "oracle-mcp-server"
      ],
      "env": {
        "ORACLE_CONNECTION_STRING": "username/password@hostname:password/service_name",
        "LIB_DIR": "D:\\tools\\instantclient19.26.0.0.0dbru\\instantclient_19_26"
      }
    }
  }
}
```

### Prerequisites

- UV (pacakge manager)
- Python 3.12+
- Cursor
- Oracle Client


