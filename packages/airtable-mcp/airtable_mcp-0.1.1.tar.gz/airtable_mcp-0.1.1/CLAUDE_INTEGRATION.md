# Claude Desktop Integration Guide

This guide provides detailed instructions for setting up the Airtable MCP with Claude Desktop.

## Prerequisites

- Claude Desktop installed
- Airtable API token
- Airtable base ID

## Configuration Steps

1. **Locate Configuration File**
   - Open Finder
   - Press `Cmd + Shift + G`
   - Enter `~/Library/Application Support/Claude`
   - Create or open `claude_desktop_config.json`

2. **Add Configuration**
   ```json
   {
     "mcpServers": {
       "airtable-mcp": {
         "command": "pipx",
         "args": [
           "airtable-mcp",
           "--token",
           "YOUR_AIRTABLE_TOKEN",
           "--base",
           "YOUR_BASE_ID"
         ]
       }
     }
   }
   ```

3. **Replace Credentials**
   - Replace `YOUR_AIRTABLE_TOKEN` with your token from [Airtable Account](https://airtable.com/account)
   - Replace `YOUR_BASE_ID` with your base ID (found in your Airtable base URL)

4. **Restart Claude Desktop**
   - Close Claude Desktop completely
   - Wait 5 seconds
   - Reopen Claude Desktop
   - Wait 30 seconds for the connection to establish

## Verification

Test the connection by asking Claude:
- "Show me all my Airtable bases"
- "What tables are in this base?"
- "Show me the first 5 records from any table"

## Troubleshooting

### Common Errors


2. **JSON Parsing Errors**
   - Remove any extra backslashes
   - Use the exact format shown above
   - Ensure no trailing commas

3. **Connection Timeout**
   - Wait full 30 seconds after startup
   - Check your internet connection
   - Verify API token is valid

## Support

If you encounter any issues:
1. Check [GitHub Issues](https://github.com/rashidazarang/airtable-mcp/issues)
2. Join our [Discord](https://discord.gg/your-discord)
3. Email: support@example.com 