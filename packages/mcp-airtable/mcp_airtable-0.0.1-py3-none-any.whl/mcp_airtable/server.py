# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Airtable MCP")

# Environment variables for Airtable configuration
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_API_URL = os.environ.get("AIRTABLE_API_URL", "https://api.airtable.com/v0")

# Check if environment variables are set
if not all([AIRTABLE_BASE_ID, AIRTABLE_API_KEY]):
    print("Warning: Airtable environment variables not fully configured. Set AIRTABLE_BASE_ID and AIRTABLE_API_KEY.", file=sys.stderr)

# Helper function for API requests
async def make_airtable_request(method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
    """
    Make a request to the Airtable API.
    
    Args:
        method: HTTP method (GET, POST, PATCH, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PATCH)
        params: Query parameters for the request
    
    Returns:
        Response from Airtable API as dictionary
    """
    url = f"{AIRTABLE_API_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method.upper() == "PATCH":
                response = await client.patch(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_info = {
                "error": True,
                "status_code": e.response.status_code,
                "message": f"HTTP Error: {e.response.status_code}"
            }
            
            try:
                error_json = e.response.json()
                error_info["details"] = error_json
            except:
                error_info["response_text"] = e.response.text
                
            return error_info
        except Exception as e:
            return {
                "error": True,
                "message": f"Error: {str(e)}"
            }

# === TOOLS ===

@mcp.tool()
async def list_bases() -> str:
    """
    List all accessible Airtable bases.
    """
    result = await make_airtable_request("GET", "/meta/bases")
    
    if result.get("error", False):
        return f"Error retrieving bases: {result.get('message', 'Unknown error')}"
    
    formatted_result = []
    for base in result.get("bases", []):
        formatted_result.append(f"Base ID: {base.get('id')}\nName: {base.get('name')}\nPermission Level: {base.get('permissionLevel')}")
    
    if not formatted_result:
        return "No bases found or insufficient permissions."
    
    return "\n\n".join(formatted_result)

@mcp.tool()
async def list_tables(base_id: Optional[str] = None) -> str:
    """
    List all tables in an Airtable base.
    
    Args:
        base_id: The Airtable base ID (if not provided, uses the default from environment variable)
    """
    base = base_id if base_id else AIRTABLE_BASE_ID
    
    if not base:
        return "Error: No base ID provided and no default base ID set in environment variables."
    
    result = await make_airtable_request("GET", f"/{base}/meta/tables")
    
    if result.get("error", False):
        return f"Error retrieving tables: {result.get('message', 'Unknown error')}"
    
    formatted_result = []
    for table in result.get("tables", []):
        fields_info = "\n".join([f"- {field.get('name')} ({field.get('type')})" for field in table.get('fields', [])])
        formatted_result.append(f"Table ID: {table.get('id')}\nName: {table.get('name')}\nPrimary Field: {table.get('primaryFieldId')}\n\nFields:\n{fields_info}")
    
    if not formatted_result:
        return "No tables found in the specified base or insufficient permissions."
    
    return "\n\n".join(formatted_result)

@mcp.tool()
async def query_records(table_name: str, max_records: int = 100, view: Optional[str] = None, filter_by_formula: Optional[str] = None, base_id: Optional[str] = None) -> str:
    """
    Query records from an Airtable table.
    
    Args:
        table_name: The name of the table to query
        max_records: Maximum number of records to return (default 100)
        view: Name of the view to use
        filter_by_formula: Airtable formula to filter records
        base_id: The Airtable base ID (if not provided, uses the default from environment variables)
    """
    base = base_id if base_id else AIRTABLE_BASE_ID
    
    if not base:
        return "Error: No base ID provided and no default base ID set in environment variables."
    
    params = {"maxRecords": max_records}
    
    if view:
        params["view"] = view
    
    if filter_by_formula:
        params["filterByFormula"] = filter_by_formula
    
    result = await make_airtable_request("GET", f"/{base}/{table_name}", params=params)
    
    if result.get("error", False):
        return f"Error querying records: {result.get('message', 'Unknown error')}"
    
    records = result.get("records", [])
    
    if not records:
        return "No records found matching your query."
    
    return json.dumps(records, indent=2)

@mcp.tool()
async def get_record(table_name: str, record_id: str, base_id: Optional[str] = None) -> str:
    """
    Get a specific record from an Airtable table.
    
    Args:
        table_name: The name of the table
        record_id: The ID of the record to retrieve
        base_id: The Airtable base ID (if not provided, uses the default from environment variables)
    """
    base = base_id if base_id else AIRTABLE_BASE_ID
    
    if not base:
        return "Error: No base ID provided and no default base ID set in environment variables."
    
    result = await make_airtable_request("GET", f"/{base}/{table_name}/{record_id}")
    
    if result.get("error", False):
        return f"Error retrieving record: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_record(table_name: str, fields: Dict[str, Any], base_id: Optional[str] = None) -> str:
    """
    Create a new record in an Airtable table.
    
    Args:
        table_name: The name of the table
        fields: Dictionary of field names and values for the new record
        base_id: The Airtable base ID (if not provided, uses the default from environment variables)
    """
    base = base_id if base_id else AIRTABLE_BASE_ID
    
    if not base:
        return "Error: No base ID provided and no default base ID set in environment variables."
    
    data = {"fields": fields}
    
    result = await make_airtable_request("POST", f"/{base}/{table_name}", data=data)
    
    if result.get("error", False):
        return f"Error creating record: {result.get('message', 'Unknown error')}"
    
    return f"Record created successfully.\n\n{json.dumps(result, indent=2)}"

@mcp.tool()
async def update_record(table_name: str, record_id: str, fields: Dict[str, Any], base_id: Optional[str] = None) -> str:
    """
    Update an existing record in an Airtable table.
    
    Args:
        table_name: The name of the table
        record_id: The ID of the record to update
        fields: Dictionary of field names and values to update
        base_id: The Airtable base ID (if not provided, uses the default from environment variables)
    """
    base = base_id if base_id else AIRTABLE_BASE_ID
    
    if not base:
        return "Error: No base ID provided and no default base ID set in environment variables."
    
    data = {"fields": fields}
    
    result = await make_airtable_request("PATCH", f"/{base}/{table_name}/{record_id}", data=data)
    
    if result.get("error", False):
        return f"Error updating record: {result.get('message', 'Unknown error')}"
    
    return f"Record updated successfully.\n\n{json.dumps(result, indent=2)}"

@mcp.tool()
async def delete_record(table_name: str, record_id: str, base_id: Optional[str] = None) -> str:
    """
    Delete a record from an Airtable table.
    
    Args:
        table_name: The name of the table
        record_id: The ID of the record to delete
        base_id: The Airtable base ID (if not provided, uses the default from environment variables)
    """
    base = base_id if base_id else AIRTABLE_BASE_ID
    
    if not base:
        return "Error: No base ID provided and no default base ID set in environment variables."
    
    result = await make_airtable_request("DELETE", f"/{base}/{table_name}/{record_id}")
    
    if result.get("error", False):
        return f"Error deleting record: {result.get('message', 'Unknown error')}"
    
    return "Record deleted successfully."

# === RESOURCES ===

@mcp.resource("airtable://tables")
async def get_tables_resource() -> str:
    """Get a list of all tables in the default Airtable base."""
    if not AIRTABLE_BASE_ID:
        return "Error: No base ID set in environment variables."
    
    result = await make_airtable_request("GET", f"/{AIRTABLE_BASE_ID}/meta/tables")
    
    if result.get("error", False):
        return f"Error retrieving tables: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("airtable://table/{table_name}")
async def get_table_schema(table_name: str) -> str:
    """Get the schema information for a specific table."""
    if not AIRTABLE_BASE_ID:
        return "Error: No base ID set in environment variables."
    
    result = await make_airtable_request("GET", f"/{AIRTABLE_BASE_ID}/meta/tables")
    
    if result.get("error", False):
        return f"Error retrieving tables: {result.get('message', 'Unknown error')}"
    
    tables = result.get("tables", [])
    target_table = next((table for table in tables if table.get("name") == table_name), None)
    
    if not target_table:
        return f"Error: Table '{table_name}' not found."
    
    return json.dumps(target_table, indent=2)

@mcp.resource("airtable://data/{table_name}")
async def get_table_data(table_name: str) -> str:
    """Get data from a specific table."""
    if not AIRTABLE_BASE_ID:
        return "Error: No base ID set in environment variables."
    
    result = await make_airtable_request("GET", f"/{AIRTABLE_BASE_ID}/{table_name}")
    
    if result.get("error", False):
        return f"Error retrieving data: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("create_record")
def create_record_prompt(table_name: str = None, fields: str = None):
    """
    A prompt template for creating a new record in Airtable.
    
    Args:
        table_name: Name of the table where to create the record
        fields: Description of the fields and values to create
    """
    if all([table_name, fields]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me create a new record in the Airtable table '{table_name}' with these fields and values:\n\n{fields}"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to create a new record in Airtable. Please help me format my data correctly for the API."
                    }
                }
            ]
        }

@mcp.prompt("query_records")
def query_records_prompt(table_name: str = None, filter_description: str = None):
    """
    A prompt template for querying records from Airtable.
    
    Args:
        table_name: Name of the table to query
        filter_description: Natural language description of the filter criteria
    """
    if all([table_name, filter_description]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me query records from the Airtable table '{table_name}' where {filter_description}. Format this as an Airtable formula and run the query."
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to query some records from my Airtable database. Please help me formulate the correct filter expression."
                    }
                }
            ]
        }

@mcp.prompt("update_record")
def update_record_prompt(table_name: str = None, record_id: str = None, update_info: str = None):
    """
    A prompt template for updating a record in Airtable.
    
    Args:
        table_name: Name of the table
        record_id: ID of the record to update
        update_info: Description of updates to make
    """
    if all([table_name, record_id, update_info]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me update record '{record_id}' in the Airtable table '{table_name}'. I want to update these fields:\n\n{update_info}"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to update an existing record in my Airtable. Please help me format the update correctly."
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Airtable MCP server...", file=sys.stderr)
    mcp.run()