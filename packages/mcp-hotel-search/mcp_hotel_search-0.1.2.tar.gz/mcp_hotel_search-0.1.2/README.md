# MCP Hotel Search

A hotel search service built with Google's Agent Developer Kit (ADK) and Model Context Protocol (MCP). This service enables AI models to search for hotels using SerpAPI .

## What is Model Context Protocol?

The Model Context Protocol (MCP) is a standard developed by Anthropic that enables AI models to use tools by defining a structured format for tool descriptions, calls, and responses. This project implements an MCP tool using Google's ADK that can be used by Claude and other MCP-compatible models.

## Installation

```bash
# Install from PyPI
pip install mcp-hotel-search

# Or install from the project directory (development mode)
git clone https://github.com/arjunprabhulal/mcp-hotel-search.git
cd mcp-hotel-search
pip install -e .
```

## Prerequisites

This project requires:
- Google's Agent Developer Kit (`google-ai-adk`)
- MCP Python SDK (`mcp-python-sdk`)
- SerpAPI API key (`google-search-results`)
- Python 3.9+

## Usage

Once installed, you can run the server using the command-line entry point:

```bash
# Ensure SERP_API_KEY is set as an environment variable or in a .env file
mcp-hotel-search
```

## Environment Variables

Set the SerpAPI key as an environment variable:

```bash
export SERP_API_KEY="your-api-key-here"
```

Alternatively, create a `.env` file in the directory where you run the server:

```
SERP_API_KEY=your_api_key_here
```

## Features

* MCP-compliant tool using Google's Agent Developer Kit (ADK) for hotel search functionality
* Integration with SerpAPI Google Hotels
* Support for searching hotels with specific check-in and check-out dates
* Packaged for easy installation and use

## MCP Tool

This package provides the following Model Context Protocol tool:

* `search_hotels`: Search for hotels with parameters:  
   * `location`: The city or location to search for hotels
   * `check_in_date`: Check-in date in YYYY-MM-DD format
   * `check_out_date`: Check-out date in YYYY-MM-DD format

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Arjun Prabhulal

For more articles on AI/ML and Generative AI, follow me on Medium: [https://medium.com/@arjun-prabhulal](https://medium.com/@arjun-prabhulal)