import sqlite3
import json
from fastmcp import FastMCP

# ----------------------------------------
# STEP A: FastMCP server banao
# ----------------------------------------
# "sales-assistant" is server ka naam hai
# Claude Desktop mein yahi naam dikhega
mcp = FastMCP("sales-assistant")

# ----------------------------------------
# STEP B: Database ka path define karo
# ----------------------------------------
DB_PATH = "/Users/mohammadfaraz/mcp-sqlite-project/sales.db"
# /Users/mohammadfaraz/mcp-sqlite-project/sales.db

# ----------------------------------------
# HELPER FUNCTION: DB se query run karna
# ----------------------------------------
# Yeh function baar baar use hoga
# Har tool ke andar yahi call hoga
def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Column names nikalo
    columns = [description[0] for description in cursor.description]
    
    # Rows nikalo
    rows = cursor.fetchall()
    conn.close()
    
    # List of dictionaries banao
    # Example: [{"month": "2024-01", "revenue": 500000}]
    result = []
    for row in rows:
        result.append(dict(zip(columns, row)))
    
    return result

# ========================================
# TOOL 1: list_tables
# ========================================
# @mcp.tool() decorator batata hai FastMCP ko
# ki yeh function ek tool hai jo Claude use kar sakta hai
@mcp.tool()
def list_tables() -> str:
    """
    Return all tables in the sales database.
    Use this when user asks what data is available.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # SQLite ka special query — saari tables ka naam
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    
    table_names = [t[0] for t in tables]
    return json.dumps({"tables": table_names})

# ========================================
# TOOL 2: show_sample_sales
# ========================================
@mcp.tool()
def show_sample_sales(limit: int = 5) -> str:
    """
    Show sample rows from sales table.
    Use this when user wants to see what the data looks like.
    limit: number of rows to return (default 5)
    """
    query = f"SELECT * FROM sales LIMIT {limit}"
    result = run_query(query)
    return json.dumps(result)

# ========================================
# TOOL 3: get_monthly_revenue
# ========================================
@mcp.tool()
def get_monthly_revenue() -> str:
    """
    Return total revenue grouped by month.
    Use this when user asks about monthly revenue,
    monthly sales trends, or month wise performance.
    """
    query = """
        SELECT 
            month,
            SUM(revenue) as total_revenue,
            SUM(units)   as total_units
        FROM sales
        GROUP BY month
        ORDER BY month
    """
    result = run_query(query)
    return json.dumps(result)

# ========================================
# TOOL 4: get_top_products
# ========================================
@mcp.tool()
def get_top_products(limit: int = 3) -> str:
    """
    Return top products by total revenue.
    Use this when user asks which product performed best,
    highest revenue product, or product ranking.
    limit: how many top products to return (default 3)
    """
    query = f"""
        SELECT 
            product,
            SUM(revenue) as total_revenue,
            SUM(units)   as total_units
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
        LIMIT {limit}
    """
    result = run_query(query)
    return json.dumps(result)

# ========================================
# SERVER START
# ========================================
if __name__ == "__main__": 
    # above line ka matlab hai ki jab yeh file directly run ho, tabhi server start hoga
    # agar yeh file kisi aur script mein import ho, toh server start nahi hoga
    # 
    print("MCP Server start...")
    print("Tools available: list_tables, show_sample_sales,")
    print("                 get_monthly_revenue, get_top_products")
    mcp.run()