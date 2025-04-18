import requests
import json
from fastmcp import FastMCP, Client

mcp = FastMCP("Dolt Database Explorer")

# Configuration - you can adjust these as needed
DOLT_API_URL = "https://www.dolthub.com/api/v1alpha1"
DATABASE_OWNER = "calvinw"  
DATABASE_NAME = "BusMgmtBenchmarks" 
DATABASE_BRANCH = "main" 

#
# def get_dolt_query_url():
#     """Get the URL for executing SQL queries against the Dolt database"""
#     return f"{DOLT_API_URL}/repos/{DATABASE_OWNER}/{DATABASE_NAME}/branches/{DATABASE_BRANCH}/sql"
#
# @mcp.resource("schema://main")
# def get_schema() -> str:
#     """Provide the database schema as a resource"""
#     try:
#         # Query to get all tables
#         tables_query = "SHOW TABLES"
#         tables_response = requests.post(
#             get_dolt_query_url(),
#             json={"q": tables_query}
#         )
#         tables_response.raise_for_status()
#         tables_data = tables_response.json()
#         
#         schema_parts = []
#         
#         # For each table, get its schema
#         for row in tables_data.get("rows", []):
#             table_name = row[0]  # Assuming first column is table name
#             
#             # Get schema for this table
#             schema_query = f"SHOW CREATE TABLE `{table_name}`"
#             schema_response = requests.post(
#                 get_dolt_query_url(),
#                 json={"q": schema_query}
#             )
#             schema_response.raise_for_status()
#             schema_data = schema_response.json()
#             
#             if schema_data.get("rows") and len(schema_data["rows"]) > 0:
#                 # Second column usually contains the CREATE TABLE statement
#                 create_statement = schema_data["rows"][0][1]
#                 schema_parts.append(create_statement)
#         
#         return "\n\n".join(schema_parts)
#     except Exception as e:
#         return f"Error retrieving schema: {str(e)}"
#
# @mcp.tool()
# def query_data(sql: str) -> str:
#     """Execute SQL queries safely on the Dolt database"""
#     try:
#         # Execute the query
#         response = requests.post(
#             get_dolt_query_url(),
#             json={"q": sql}
#         )
#         response.raise_for_status()
#         result = response.json()
#         
#         # Format the result
#         if "rows" not in result:
#             return "No data returned or query doesn't return rows."
#         
#         # Get column names from the result
#         columns = result.get("columnDescriptions", [])
#         column_names = [col.get("name", f"Column{i}") for i, col in enumerate(columns)]
#         
#         # Create header row
#         output = [" | ".join(column_names)]
#         output.append("-" * len(" | ".join(column_names)))
#         
#         # Add data rows
#         for row in result["rows"]:
#             # Convert all values to strings and handle None/null values
#             row_values = [str(val) if val is not None else "NULL" for val in row]
#             output.append(" | ".join(row_values))
#         
#         return "\n".join(output)
#     except Exception as e:
#         return f"Error executing query: {str(e)}"
#
# @mcp.tool()
# def list_tables() -> str:
#     """List all tables in the database"""
#     try:
#         response = requests.post(
#             get_dolt_query_url(),
#             json={"q": "SHOW TABLES"}
#         )
#         response.raise_for_status()
#         result = response.json()
#         
#         if "rows" not in result or not result["rows"]:
#             return "No tables found."
#         
#         tables = [row[0] for row in result["rows"]]
#         return "\n".join(tables)
#     except Exception as e:
#         return f"Error listing tables: {str(e)}"
#
# @mcp.tool()
# def describe_table(table_name: str) -> str:
#     """Describe the structure of a specific table"""
#     try:
#         response = requests.post(
#             get_dolt_query_url(),
#             json={"q": f"DESCRIBE `{table_name}`"}
#         )
#         response.raise_for_status()
#         result = response.json()
#         
#         if "rows" not in result or not result["rows"]:
#             return f"Table '{table_name}' not found or is empty."
#         
#         # Get column descriptions
#         columns = result.get("columnDescriptions", [])
#         column_names = [col.get("name", f"Column{i}") for i, col in enumerate(columns)]
#         
#         # Format the results
#         output = [" | ".join(column_names)]
#         output.append("-" * len(" | ".join(column_names)))
#         
#         for row in result["rows"]:
#             row_values = [str(val) if val is not None else "NULL" for val in row]
#             output.append(" | ".join(row_values))
#         
#         return "\n".join(output)
#     except Exception as e:
#         return f"Error describing table: {str(e)}"

# Keep the original greeting function
@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

def main():
    print("Dolt Database Explorer MCP Server is running")
    print(f"Connected to: {DATABASE_OWNER}/{DATABASE_NAME}, branch: {DATABASE_BRANCH}")
    mcp.run()
