import logging
import json
from typing import Any, List

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
from pydantic import AnyUrl, ValidationError

from syne_ga_mcp.config import Config
from syne_ga_mcp.ga_handler import GA4Client

logger = logging.getLogger("syne_ga_mcp")
logger.setLevel(logging.INFO) # Or DEBUG for more verbose logs
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

async def main(config: Config):
    logger.info(f"Starting Google Analytics MCP Server for property: {config.property_id}")

    try:
        ga_client = GA4Client(default_property_id=config.property_id, service_account_info=config.service_account_info)
        await ga_client.verify_auth()
        logger.info("Google Analytics client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Google Analytics client: {e}")
        # Exit or handle the error appropriately if GA connection is critical
        return

    server = Server("syne_ga_mcp")

    logger.debug("Registering handlers")

    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        return [] # No specific resources defined for now

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        return "No resource content available."

    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        return [] # No specific prompts defined for now

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
        return types.GetPromptResult(description="No prompts available.", messages=[])

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available Google Analytics tools."""
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
        return tools

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests for Google Analytics."""
        logger.info(f"Received tool call: {name} with arguments: {arguments}")
        
        if not arguments:
            logger.error(f"Missing arguments for tool call: {name}")
            return [types.TextContent(type="text", text=f"Error: Missing arguments for {name}")]

        try:
            if name == "run_ga4_report":
                # Extract arguments
                metrics = arguments.get("metrics")
                dimensions = arguments.get("dimensions")
                date_range = arguments.get("date_range", "last30days")
                limit = arguments.get("limit", 10)

                # Basic validation
                if not metrics:
                    raise ValueError("'metrics' argument is required.")
                
                logger.info(f"Running GA4 report with date range: {date_range}")
                results = await ga_client.run_report(
                    metrics=metrics,
                    dimensions=dimensions,
                    date_range=date_range,
                    limit=limit
                )
                return [types.TextContent(type="text", text=json.dumps(results, indent=2))]
            
            elif name == "run_realtime_report":
                metrics = arguments.get("metrics")
                dimensions = arguments.get("dimensions")
                limit = arguments.get("limit", 10)

                if not metrics:
                    raise ValueError("'metrics' argument is required.")
                
                logger.info(f"Running GA4 realtime report")
                results = await ga_client.run_realtime_report(
                    metrics=metrics,
                    dimensions=dimensions,
                    limit=limit
                )
                return [types.TextContent(type="text", text=json.dumps(results, indent=2))]

            elif name == "get_metadata":
                metadata_type = arguments.get("metadata_type", "all")
                
                logger.info(f"Getting GA4 metadata for type: {metadata_type}")
                results = await ga_client.get_metadata(
                    metadata_type=metadata_type
                )
                return [types.TextContent(type="text", text=json.dumps(results, indent=2))]

            else:
                logger.warning(f"Unknown tool called: {name}")
                return [types.TextContent(type="text", text=f"Error: Unknown tool '{name}'")]

        except ValidationError as e:
            logger.error(f"Validation error calling {name}: {e}")
            return [types.TextContent(type="text", text=f"Input Validation Error: {e}")]
        except ValueError as e:
            logger.error(f"Value error calling {name}: {e}")
            return [types.TextContent(type="text", text=f"Error: {e}")]
        except Exception as e:
            logger.error(f"Unexpected error calling {name}: {e}", exc_info=True)
            return [types.TextContent(type="text", text=f"An unexpected error occurred: {e}")]

    # Run the server using stdin/stdout streams
    options = server.create_initialization_options()
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Google Analytics MCP Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            options,
        )
