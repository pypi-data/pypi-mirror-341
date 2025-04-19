# Airtable MCP Server

A Model Context Protocol (MCP) server for Airtable integration. This server provides tools for interacting with Airtable, including querying tables, managing records, and performing various operations against the Airtable API.

## Features

- **Table Management**: List and explore tables in your Airtable bases
- **Record Operations**: Create, read, update, and delete records
- **Query Capabilities**: Filter and search records using Airtable formulas
- **Resources**: Access metadata about Airtable tables and schemas
- **Prompts**: Templates for common Airtable workflows

## Installation

```bash
pip install mcp-airtable
```

## Configuration

Set the following environment variables:

```bash
export AIRTABLE_BASE_ID="your_base_id"
export AIRTABLE_API_KEY="your_api_token"
```

Optional configuration:
```bash
export AIRTABLE_API_URL="https://api.airtable.com/v0"  # Default API URL
```

## Usage

### Starting the server directly

```bash
mcp-airtable
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcp-airtable": {
  "command": "uvx",
  "args": [
    "mcp-airtable"
  ],
  "env": {
    "AIRTABLE_BASE_ID": "your_base_id",
    "AIRTABLE_API_KEY": "your_api_token"
  }
}
```

Replace the environment variables with your actual Airtable credentials.

## Available Tools

### Base and Table Management

* **list_bases**: Get a list of all accessible Airtable bases
* **list_tables**: List all tables in a specific Airtable base

### Record Operations

* **query_records**: Query records from a table with optional filtering
* **get_record**: Get a specific record by ID
* **create_record**: Create a new record in a table
* **update_record**: Update an existing record in a table
* **delete_record**: Delete a record from a table

## Available Resources

* **airtable://tables**: List of all tables in the default Airtable base
* **airtable://table/{table_name}**: Schema information for a specific table
* **airtable://data/{table_name}**: Data from a specific table

## Available Prompts

* **create_record**: Template for creating a new record
* **query_records**: Template for querying records with filtering
* **update_record**: Template for updating an existing record

## Example Usage

### Querying records

```
Can you show me all records from my "Contacts" table where the status is "Active"?
```

### Creating a new record

```
Create a new record in the "Projects" table with name "New Website", status "Planning", and due date "2023-12-31"
```

### Updating a record

```
Update the record with ID "recABC123" in the "Tasks" table to change its status to "Completed"
```

## Development

Clone the repository and install development dependencies:

```bash
git clone https://github.com/yourusername/mcp-airtable.git
cd mcp-airtable
pip install -e ".[dev]"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Version

0.0.1
