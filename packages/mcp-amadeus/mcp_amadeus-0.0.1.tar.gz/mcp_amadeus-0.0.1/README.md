# Amadeus MCP Server

A Model Context Protocol (MCP) server for Amadeus API integration. This server provides tools for interacting with Amadeus travel-related services, including flight search, hotel booking, and airport information.

## Features

- **Flight Search**: Search for available flights between destinations
- **Hotel Booking**: Find accommodations in specific cities
- **Airport & City Information**: Get details about airports and cities
- **Travel Planning Assistance**: Prompts for common travel workflows

## Installation

```bash
pip install mcp-amadeus
```

## Configuration

Set the following environment variables:

```bash
export AMADEUS_CLIENT_ID="your_client_id"
export AMADEUS_CLIENT_SECRET="your_client_secret"
export AMADEUS_BASE_URL="https://test.api.amadeus.com/v1"  # Use test or production URL
```

## Usage

### Starting the server directly

```bash
mcp-amadeus
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcp-amadeus": {
  "command": "uvx",
  "args": [
    "mcp-amadeus"
  ],
  "env": {
    "AMADEUS_CLIENT_ID": "your_client_id",
    "AMADEUS_CLIENT_SECRET": "your_client_secret",
    "AMADEUS_BASE_URL": "https://test.api.amadeus.com/v1"
  }
}
```

Replace the environment variables with your actual Amadeus API credentials.

## Available Tools

* **search_flights**: Search for flight options between destinations
* **search_hotels**: Search for hotel options in a city
* **get_airport_info**: Get information about an airport by its IATA code
* **get_city_info**: Get information about a city by its IATA code
* **get_flight_offers_price**: Get pricing for specific flight offers

## Available Resources

* **amadeus://airports**: List of popular airports
* **amadeus://cities**: List of popular cities

## Available Prompts

* **plan_trip**: Template for planning a complete trip with flights and accommodations
* **find_flight**: Template for finding a flight between two locations
* **find_hotel**: Template for finding accommodations in a specific location

## Authentication

This MCP server implements OAuth 2.0 authentication with the Amadeus API using client credentials. The token is automatically managed and refreshed as needed.

## Error Handling

The server includes robust error handling for:
- API authentication failures
- Invalid requests
- Server errors
- Network issues

## Version

0.0.1

## License

MIT
