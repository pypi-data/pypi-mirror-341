# server.py
import sys
import os
import json
import httpx
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Amadeus MCP")

# Environment variables for Amadeus configuration
AMADEUS_BASE_URL = os.environ.get("AMADEUS_BASE_URL", "https://test.api.amadeus.com/v1")
AMADEUS_CLIENT_ID = os.environ.get("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.environ.get("AMADEUS_CLIENT_SECRET")

# Check if environment variables are set
if not all([AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET]):
    print("Warning: Amadeus environment variables not fully configured. Set AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET.", file=sys.stderr)

# Token storage
_token_data = {
    "access_token": None,
    "expires_at": 0
}

# Helper function to get access token
async def get_access_token() -> str:
    """Get a valid access token for Amadeus API."""
    import time
    
    # Check if we have a valid token
    current_time = time.time()
    if _token_data["access_token"] and _token_data["expires_at"] > current_time:
        return _token_data["access_token"]
    
    # Get a new token
    auth_url = f"{AMADEUS_BASE_URL.split('/v1')[0]}/v1/security/oauth2/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_CLIENT_ID,
        "client_secret": AMADEUS_CLIENT_SECRET
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            auth_url,
            data=auth_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code != 200:
            print(f"Error getting Amadeus access token: {response.text}", file=sys.stderr)
            return None
        
        token_info = response.json()
        _token_data["access_token"] = token_info["access_token"]
        _token_data["expires_at"] = current_time + token_info["expires_in"] - 60  # Buffer of 60 seconds
        
        return _token_data["access_token"]

# Helper function for API requests
async def make_amadeus_request(method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
    """
    Make a request to the Amadeus API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
        params: Query parameters (for GET)
    
    Returns:
        Response from Amadeus API as dictionary
    """
    access_token = await get_access_token()
    if not access_token:
        return {"error": True, "message": "Failed to authenticate with Amadeus API"}
    
    url = f"{AMADEUS_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data, timeout=30.0)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code >= 400:
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": response.text
                }
                
            return response.json()
    except Exception as e:
        return {
            "error": True,
            "message": f"Request failed: {str(e)}"
        }

# === TOOLS ===

@mcp.tool()
async def search_flights(origin: str, destination: str, departure_date: str, return_date: str = None, adults: int = 1, currency: str = "USD") -> str:
    """
    Search for available flights between two locations.
    
    Args:
        origin: Origin location code (IATA airport or city code)
        destination: Destination location code (IATA airport or city code)
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format (for round trips)
        adults: Number of adult passengers
        currency: Preferred currency for prices (default: USD)
    """
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "currencyCode": currency,
        "max": 5  # Limit to 5 results for readability
    }
    
    if return_date:
        params["returnDate"] = return_date
    
    result = await make_amadeus_request("GET", "/shopping/flight-offers", params=params)
    
    if result.get("error"):
        return f"Error searching flights: {result.get('message', 'Unknown error')}"
    
    # Format the results in a more readable way
    flight_offers = result.get("data", [])
    if not flight_offers:
        return "No flights found matching your criteria."
    
    formatted_results = []
    for offer in flight_offers:
        price = offer.get("price", {}).get("total", "N/A")
        currency = offer.get("price", {}).get("currency", currency)
        
        itineraries = []
        for itinerary in offer.get("itineraries", []):
            segments = []
            for segment in itinerary.get("segments", []):
                departure = segment.get("departure", {})
                arrival = segment.get("arrival", {})
                carrier = segment.get("carrierCode", "")
                
                segments.append(f"{departure.get('iataCode', '')} → {arrival.get('iataCode', '')} ({carrier})")
            
            itineraries.append(" | ".join(segments))
        
        formatted_results.append(
            f"Price: {price} {currency}\n"
            f"Outbound: {itineraries[0] if itineraries else 'N/A'}\n"
            f"{'Return: ' + itineraries[1] if len(itineraries) > 1 else ''}"
        )
    
    return "\n\n".join(formatted_results)

@mcp.tool()
async def search_hotels(city_code: str, check_in_date: str, check_out_date: str, adults: int = 1, ratings: str = None, currency: str = "USD") -> str:
    """
    Search for available hotels in a city.
    
    Args:
        city_code: City code (IATA code)
        check_in_date: Check-in date in YYYY-MM-DD format
        check_out_date: Check-out date in YYYY-MM-DD format
        adults: Number of adult guests
        ratings: Comma-separated list of ratings (1-5)
        currency: Preferred currency for prices (default: USD)
    """
    params = {
        "cityCode": city_code,
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "adults": adults,
        "currency": currency,
        "includeClosed": "false",
        "bestRateOnly": "true",
        "view": "FULL"
    }
    
    if ratings:
        params["ratings"] = ratings
    
    result = await make_amadeus_request("GET", "/shopping/hotel-offers", params=params)
    
    if result.get("error"):
        return f"Error searching hotels: {result.get('message', 'Unknown error')}"
    
    # Format the results in a more readable way
    hotel_offers = result.get("data", [])
    if not hotel_offers:
        return "No hotels found matching your criteria."
    
    formatted_results = []
    for offer in hotel_offers[:5]:  # Limit to 5 results for readability
        hotel = offer.get("hotel", {})
        name = hotel.get("name", "Unknown Hotel")
        rating = hotel.get("rating", "N/A")
        
        offer_details = offer.get("offers", [{}])[0] if offer.get("offers") else {}
        price = offer_details.get("price", {}).get("total", "N/A")
        currency = offer_details.get("price", {}).get("currency", currency)
        
        formatted_results.append(
            f"Hotel: {name}\n"
            f"Rating: {rating}\n"
            f"Price: {price} {currency} (total stay)"
        )
    
    return "\n\n".join(formatted_results)

@mcp.tool()
async def get_airport_info(airport_code: str) -> str:
    """
    Get information about an airport by its IATA code.
    
    Args:
        airport_code: IATA airport code (e.g., JFK, LHR)
    """
    params = {
        "airportCode": airport_code
    }
    
    result = await make_amadeus_request("GET", f"/reference-data/locations/A{airport_code}", params=params)
    
    if result.get("error"):
        return f"Error retrieving airport information: {result.get('message', 'Unknown error')}"
    
    data = result.get("data", {})
    if not data:
        return f"No information found for airport code {airport_code}."
    
    name = data.get("name", "N/A")
    city = data.get("address", {}).get("cityName", "N/A")
    country = data.get("address", {}).get("countryName", "N/A")
    location = data.get("geoCode", {})
    latitude = location.get("latitude", "N/A")
    longitude = location.get("longitude", "N/A")
    
    return (
        f"Airport: {name} ({airport_code})\n"
        f"City: {city}\n"
        f"Country: {country}\n"
        f"Location: {latitude}, {longitude}"
    )

@mcp.tool()
async def get_city_info(city_code: str) -> str:
    """
    Get information about a city by its IATA code.
    
    Args:
        city_code: IATA city code (e.g., NYC, LON)
    """
    params = {
        "cityCode": city_code,
        "view": "FULL"
    }
    
    result = await make_amadeus_request("GET", f"/reference-data/locations/C{city_code}", params=params)
    
    if result.get("error"):
        return f"Error retrieving city information: {result.get('message', 'Unknown error')}"
    
    data = result.get("data", {})
    if not data:
        return f"No information found for city code {city_code}."
    
    name = data.get("name", "N/A")
    country = data.get("address", {}).get("countryName", "N/A")
    location = data.get("geoCode", {})
    latitude = location.get("latitude", "N/A")
    longitude = location.get("longitude", "N/A")
    
    return (
        f"City: {name} ({city_code})\n"
        f"Country: {country}\n"
        f"Location: {latitude}, {longitude}"
    )

@mcp.tool()
async def get_flight_offers_price(offer_ids: str) -> str:
    """
    Get pricing information for specific flight offers.
    
    Args:
        offer_ids: Comma-separated list of flight offer IDs
    """
    # This would typically take the flight offer objects and confirm pricing
    # For simplicity, we're just returning a message
    return "The pricing feature requires full flight offer objects that are obtained from a flight search."

# === RESOURCES ===

@mcp.resource("amadeus://airports")
async def get_popular_airports() -> str:
    """Get a list of popular airports."""
    # Predefined list of popular airports with codes
    popular_airports = [
        {"code": "JFK", "name": "John F. Kennedy International Airport", "city": "New York"},
        {"code": "LHR", "name": "London Heathrow Airport", "city": "London"},
        {"code": "CDG", "name": "Charles de Gaulle Airport", "city": "Paris"},
        {"code": "LAX", "name": "Los Angeles International Airport", "city": "Los Angeles"},
        {"code": "DXB", "name": "Dubai International Airport", "city": "Dubai"},
        {"code": "HND", "name": "Tokyo Haneda Airport", "city": "Tokyo"},
        {"code": "SIN", "name": "Singapore Changi Airport", "city": "Singapore"},
        {"code": "SYD", "name": "Sydney Airport", "city": "Sydney"},
        {"code": "FRA", "name": "Frankfurt Airport", "city": "Frankfurt"},
        {"code": "IST", "name": "Istanbul Airport", "city": "Istanbul"}
    ]
    
    return json.dumps(popular_airports, indent=2)

@mcp.resource("amadeus://cities")
async def get_popular_cities() -> str:
    """Get a list of popular cities."""
    # Predefined list of popular cities with codes
    popular_cities = [
        {"code": "NYC", "name": "New York", "country": "United States"},
        {"code": "LON", "name": "London", "country": "United Kingdom"},
        {"code": "PAR", "name": "Paris", "country": "France"},
        {"code": "TYO", "name": "Tokyo", "country": "Japan"},
        {"code": "ROM", "name": "Rome", "country": "Italy"},
        {"code": "BKK", "name": "Bangkok", "country": "Thailand"},
        {"code": "SYD", "name": "Sydney", "country": "Australia"},
        {"code": "BER", "name": "Berlin", "country": "Germany"},
        {"code": "DXB", "name": "Dubai", "country": "United Arab Emirates"},
        {"code": "HKG", "name": "Hong Kong", "country": "China"}
    ]
    
    return json.dumps(popular_cities, indent=2)

# === PROMPTS ===

@mcp.prompt("plan_trip")
def plan_trip_prompt(origin: str = None, destination: str = None, departure_date: str = None, return_date: str = None):
    """
    A prompt template for planning a complete trip with flights and accommodations.
    
    Args:
        origin: Origin location
        destination: Destination location
        departure_date: Departure date
        return_date: Return date
    """
    details = ""
    if all([origin, destination, departure_date]):
        details = f"""
Origin: {origin}
Destination: {destination}
Departure date: {departure_date}
Return date: {return_date or "One-way trip"}
"""
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"I need help planning a trip{' with these details:' if details else '.'}\n\n{details}\n\nPlease help me search for flights and accommodations."
                }
            }
        ]
    }

@mcp.prompt("find_flight")
def find_flight_prompt(origin: str = None, destination: str = None, date: str = None):
    """
    A prompt template for finding a flight.
    
    Args:
        origin: Origin location
        destination: Destination location
        date: Travel date
    """
    details = ""
    if all([origin, destination, date]):
        details = f"""
Origin: {origin}
Destination: {destination}
Date: {date}
"""
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"I need to find a flight{' with these details:' if details else '.'}\n\n{details}\n\nCan you help me search for available options?"
                }
            }
        ]
    }

@mcp.prompt("find_hotel")
def find_hotel_prompt(location: str = None, check_in: str = None, check_out: str = None):
    """
    A prompt template for finding a hotel.
    
    Args:
        location: Hotel location
        check_in: Check-in date
        check_out: Check-out date
    """
    details = ""
    if all([location, check_in, check_out]):
        details = f"""
Location: {location}
Check-in: {check_in}
Check-out: {check_out}
"""
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"I need to find a hotel{' with these details:' if details else '.'}\n\n{details}\n\nCan you help me search for available options?"
                }
            }
        ]
    }

if __name__ == "__main__":
    print("Starting Amadeus MCP server...", file=sys.stderr)
    mcp.run()
