#!/usr/bin/env python3
"""
Hotel Search MCP Server

An MCP server that implements hotel search functionality using Google's Agent Developer Kit (ADK) wrapper.
"""
import asyncio
import json
import os
from dotenv import load_dotenv
from typing import Dict
from datetime import datetime
from serpapi import GoogleSearch

# MCP Server Imports
from mcp import types as mcp_types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# ADK Tool Imports
from google.adk.tools.function_tool import FunctionTool
# ADK <-> MCP Conversion Utility
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# --- Load Environment Variables ---
load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY", "your_serpapi_key_here")

# --- Define Hotel Search Function for ADK Tool ---
async def search_hotels(location: str, check_in_date: str, check_out_date: str) -> Dict:
    """Search for hotels using SerpAPI's Google Hotels integration."""
    
    if not SERP_API_KEY or SERP_API_KEY == "your_serpapi_key_here":
        return {"error": "SERP_API_KEY not configured"}
    
    # Validate dates
    try:
        check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
        if check_out <= check_in:
            return {"error": "Check-out date must be after check-in date"}
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    
    # Configure SerpAPI parameters
    params = {
        "api_key": SERP_API_KEY,
        "engine": "google_hotels",
        "q": location,
        "hl": "en",
        "gl": "us",
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "currency": "USD"
    }
    
    try:
        # Run the search
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Process and format the results
        if "error" in results:
            return {"error": results["error"]}
        
        hotel_properties = results.get("properties", [])
        if not hotel_properties:
            return {"results": [], "message": "No hotels found for this search"}
        
        formatted_hotels = []
        for hotel in hotel_properties[:10]:  # Limit to top 10 results
            formatted_hotel = {
                "name": hotel.get("name", "Unknown"),
                "price": hotel.get("rate_per_night", {}).get("lowest", "Price not available"),
                "rating": hotel.get("overall_rating", 0),
                "reviews": hotel.get("reviews", 0),
                "location": hotel.get("address", "Location not available"),
                "description": hotel.get("description", "No description available"),
                "images": "No image available"
            }
                
            # Get image if available
            if hotel.get("images") and len(hotel["images"]) > 0:
                formatted_hotel["images"] = hotel["images"][0].get("thumbnail", "No image available")
                
            formatted_hotels.append(formatted_hotel)
        
        return {
            "results": formatted_hotels,
            "count": len(formatted_hotels),
            "location": location,
            "dates": f"{check_in_date} to {check_out_date}"
        }
            
    except Exception as e:
        return {"error": f"Hotel search failed: {str(e)}"}

# --- Prepare the ADK Tool ---
print("Initializing ADK hotel search tool...")
hotel_search_tool = FunctionTool(search_hotels)
print(f"ADK tool '{hotel_search_tool.name}' initialized.")
# --- End ADK Tool Prep ---

# --- MCP Server Setup ---
print("Creating MCP Server instance...")
# Create a named MCP Server instance
app = Server("hotel-search-mcp-server")

# Implement the MCP server's list_tools handler
@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """MCP handler to list available tools."""
    print("MCP Server: Received list_tools request.")
    # Convert the ADK tool's definition to MCP format
    mcp_tool_schema = adk_to_mcp_tool_type(hotel_search_tool)
    print(f"MCP Server: Advertising tool: {mcp_tool_schema.name}")
    return [mcp_tool_schema]

# Implement the MCP server's call_tool handler
@app.call_tool()
async def call_tool(
    name: str, arguments: dict
) -> list[mcp_types.TextContent | mcp_types.ImageContent | mcp_types.EmbeddedResource]:
    """MCP handler to execute a tool call."""
    print(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")

    # Check if the requested tool name matches our wrapped ADK tool
    if name == hotel_search_tool.name:
        try:
            # Execute the ADK tool's run_async method
            adk_response = await hotel_search_tool.run_async(
                args=arguments,
                tool_context=None,  # No ADK context available here
            )
            print(f"MCP Server: ADK tool '{name}' executed successfully.")
            
            # Format the ADK tool's response as JSON
            response_text = json.dumps(adk_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            print(f"MCP Server: Error executing ADK tool '{name}': {e}")
            error_text = json.dumps({"error": f"Failed to execute tool '{name}': {str(e)}"})
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        # Handle calls to unknown tools
        print(f"MCP Server: Tool '{name}' not found.")
        error_text = json.dumps({"error": f"Tool '{name}' not implemented."})
        return [mcp_types.TextContent(type="text", text=error_text)]

# --- MCP Server Runner ---
async def run_server():
    """Runs the MCP server over standard input/output."""
    # Use the stdio_server context manager from the MCP library
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        print("MCP Server starting handshake...")
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        print("MCP Server run loop finished.")

def main():
    """Main entry point for the server script."""
    print("Launching Hotel Search MCP Server...")
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nMCP Server stopped by user.")
    except Exception as e:
        print(f"MCP Server encountered an error: {e}")
    finally:
        print("MCP Server process exiting.")

if __name__ == "__main__":
    main()
# --- End MCP Server ---