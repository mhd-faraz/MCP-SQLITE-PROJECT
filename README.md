# MCP SQLite Sales Assistant

A Model Context Protocol (MCP) server that connects 
Claude Desktop to a SQLite sales database.

## What it does
Ask Claude natural language questions about sales data:
- "Which product generated the most revenue?"
- "What is my monthly revenue trend?"
- "Show me sample data"

## Project Structure
mcp-sqlite-project/
├── create_db.py      # Creates SQLite database with sales data
├── mcp_server.py     # MCP server with 4 tools
└── sales.db          # Auto-generated (run create_db.py)

## Setup

### 1. Install dependencies
pip3 install fastmcp pandas

### 2. Create database
python3 create_db.py

### 3. Configure Claude Desktop
Add to claude_desktop_config.json:
{
  "mcpServers": {
    "sales-assistant": {
      "command": "/your/path/to/python3",
      "args": ["/your/path/to/mcp_server.py"]
    }
  }
}

### 4. Restart Claude Desktop

## Tools Available
- list_tables — Show all database tables
- show_sample_sales — Show sample rows
- get_monthly_revenue — Monthly revenue trends  
- get_top_products — Top products by revenue

## Built with
- FastMCP
- SQLite
- Pandas
- Claude Desktop
