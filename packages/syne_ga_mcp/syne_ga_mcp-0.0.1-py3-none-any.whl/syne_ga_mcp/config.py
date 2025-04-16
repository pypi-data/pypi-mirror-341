import argparse
import base64
from dataclasses import dataclass
import json
from typing import List
import typer
from pydantic import BaseModel, Field, EmailStr, SecretStr

@dataclass
class Config:
    """Configuration for the Google Analytics MCP Server."""

    property_id: str = Field(..., description="Google Analytics Property ID (e.g., 123456789)")
    service_account_info: dict = Field(..., description="Base64 encoded service account info")

    @staticmethod
    def from_arguments() -> "Config":
        """
        Parse command line arguments.
        """
        parser = argparse.ArgumentParser(description="Google Analytics MCP Server")

        parser.add_argument(
            "--property-id",
            type=str,
            help="Google Analytics Property ID (e.g., 123456789)",
            required=True,
        )

        parser.add_argument(
            "--service-account-info",
            type=str,
            help="Base64 encoded service account info",
            required=True,
        )

        args = parser.parse_args()

        return Config(
            property_id=args.property_id,
            service_account_info=json.loads(base64.b64decode(args.service_account_info).decode("utf-8")),
        )
