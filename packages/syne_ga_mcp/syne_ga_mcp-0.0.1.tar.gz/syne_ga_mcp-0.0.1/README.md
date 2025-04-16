# Syne Google Analytics MCP Server

A Model Context Protocol (MCP) server for Google Analytics 4 data.

## Overview

This server provides an MCP interface to Google Analytics 4 data, allowing AI assistants to query GA4 data through a standardized protocol.

## Features

The server exposes the following tools via the MCP `call_tool` endpoint:

- **`run_ga4_report`**: Runs a standard report using the Google Analytics Data API v1beta. Allows specifying metrics, optional dimensions, date range, and row limit.
- **`run_realtime_report`**: Runs a realtime report using the Google Analytics Data API v1beta. Allows specifying metrics, optional dimensions, and row limit.
- **`get_metadata`**: Gets metadata about available metrics and dimensions (or all) for the configured GA4 property.

It also handles authentication using Google service account credentials provided in the configuration.



```python
        tools = [
            types.Tool(
                name="run_ga4_report",
                description="Runs a report using the Google Analytics Data API v1beta.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "metrics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Required. List of metric names (e.g., ['activeUsers', 'sessions']). See GA4 documentation for valid metrics."
                        },
                        "dimensions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional. List of dimension names (e.g., ['country', 'city']). See GA4 documentation for valid dimensions.",
                            "optional": True
                        },
                        "date_range": {
                            "type": "string", # Could also be an object, handled by ga_handler
                            "description": "Optional. Date range alias ('today', 'yesterday', 'last7days', 'last30days') or an object like {'start_date': 'YYYY-MM-DD', 'end_date': 'YYYY-MM-DD'}.",
                            "default": "last30days"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Optional. The maximum number of rows to return in the report.",
                            "default": 10
                        }
                    },
                    "required": ["metrics"]
                },
            ),
            types.Tool(
                name="run_realtime_report",
                description="Runs a realtime report using the Google Analytics Data API v1beta.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "metrics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Required. List of metric names (e.g., ['activeUsers', 'screenPageViews']). See GA4 realtime documentation for valid metrics."
                        },
                        "dimensions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional. List of dimension names (e.g., ['country', 'city']). See GA4 realtime documentation for valid dimensions.",
                            "optional": True
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Optional. The maximum number of rows to return in the report.",
                            "default": 10
                        }
                    },
                    "required": ["metrics"]
                },
            ),
            types.Tool(
                name="get_metadata",
                description="Gets metadata about available metrics and dimensions for the configured property.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "metadata_type": {
                            "type": "string",
                            "description": "Optional. Specifies the type of metadata to retrieve: 'metrics', 'dimensions', or 'all'.",
                            "default": "all",
                            "enum": ["metrics", "dimensions", "all"] # Adding enum for clarity
                        }
                    }
                },
            ),
        ]
```

