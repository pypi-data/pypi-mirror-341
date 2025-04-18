import requests
import json
from fastmcp import FastMCP, Client

mcp = FastMCP("Dolt Database Explorer")

# Configuration - you can adjust these as needed
DOLT_API_URL = "https://www.dolthub.com/api/v1alpha1"
DATABASE_OWNER = "calvinw"  
DATABASE_NAME = "coffee-shop" 
DATABASE_BRANCH = "main" 

def get_dolt_query_url():
    """Get the URL for executing SQL queries against the Dolt database"""
    return f"{DOLT_API_URL}/{DATABASE_OWNER}/{DATABASE_NAME}/{DATABASE_BRANCH}"

@mcp.resource("schema://main")
def get_schema() -> str:
    """Provide the database schema as a resource"""
    try:
        # Query to get all tables
        tables_query = "SHOW TABLES"
        tables_response = requests.get(
            get_dolt_query_url(),
            params={"q": tables_query}
        )
        tables_response.raise_for_status()
        tables_data = tables_response.json()

        schema_parts = []

        # For each table, get its schema
        for row in tables_data.get("rows", []):
            # Extract table name from the row object based on JSON structure
            table_name = row.get(f"Tables_in_{DATABASE_NAME}")

            if table_name:
                # Get schema for this table
                schema_query = f"SHOW CREATE TABLE `{table_name}`"
                schema_response = requests.get(
                    get_dolt_query_url(),
                    params={"q": schema_query}
                )
                schema_response.raise_for_status()
                schema_data = schema_response.json()

                if schema_data.get("rows") and len(schema_data["rows"]) > 0:
                    # Extract Create Table statement from the response
                    create_statement = schema_data["rows"][0].get("Create Table")
                    if create_statement:
                        schema_parts.append(create_statement)

        return "\n\n".join(schema_parts)
    except Exception as e:
        return f"Error retrieving schema: {str(e)}"

@mcp.tool()
def query_data(sql: str) -> str:
    """Execute SQL queries safely on the Dolt database"""
    try:
        # Execute the query
        response = requests.get(
            get_dolt_query_url(),
            params={"q": sql}
        )
        response.raise_for_status()
        result = response.json()

        # Format the result
        if "rows" not in result or not result["rows"]:
            return "No data returned or query doesn't return rows."

        # Get column names from the schema
        columns = result.get("schema", [])
        column_names = [col.get("columnName", f"Column{i}") for i, col in enumerate(columns)]

        # Create header row
        output = [" | ".join(column_names)]
        output.append("-" * len(" | ".join(column_names)))

        # Add data rows
        for row in result["rows"]:
            # Get values in the same order as column names
            row_values = []
            for col_name in column_names:
                val = row.get(col_name)
                row_values.append(str(val) if val is not None else "NULL")
            output.append(" | ".join(row_values))

        return "\n".join(output)
    except Exception as e:
        return f"Error executing query: {str(e)}"

@mcp.tool()
def list_tables() -> str:
    """List all tables in the database"""
    try:
        response = requests.get(
            get_dolt_query_url(),
            params={"q": "SHOW TABLES"}
        )
        response.raise_for_status()
        result = response.json()

        if "rows" not in result or not result["rows"]:
            return "No tables found."

        # Extract table names from the rows
        table_column_name = f"Tables_in_{DATABASE_NAME}"
        tables = [row.get(table_column_name) for row in result["rows"] 
                 if row.get(table_column_name)]
        
        return "\n".join(tables)
    except Exception as e:
        return f"Error listing tables: {str(e)}"

@mcp.tool()
def describe_table(table_name: str) -> str:
    """Describe the structure of a specific table"""
    try:
        response = requests.get(
            get_dolt_query_url(),
            params={"q": f"DESCRIBE `{table_name}`"}
        )
        response.raise_for_status()
        result = response.json()

        if "rows" not in result or not result["rows"]:
            return f"Table '{table_name}' not found or is empty."

        # Get column names from the schema
        columns = result.get("schema", [])
        column_names = [col.get("columnName", f"Column{i}") for i, col in enumerate(columns)]

        # Format the results
        output = [" | ".join(column_names)]
        output.append("-" * len(" | ".join(column_names)))

        # Add data rows
        for row in result["rows"]:
            # Get values in the same order as column names
            row_values = []
            for col_name in column_names:
                val = row.get(col_name)
                row_values.append(str(val) if val is not None else "NULL")
            output.append(" | ".join(row_values))

        return "\n".join(output)
    except Exception as e:
        return f"Error describing table: {str(e)}"

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

def main():
    print("Dolt Database Explorer MCP Server is running")
    print(f"Connected to: {DATABASE_OWNER}/{DATABASE_NAME}, branch: {DATABASE_BRANCH}")
    mcp.run()
