# server.py

from enum import Enum
import json
from typing import Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from pydantic import BaseModel


class MathTools(str, Enum):
    INT_ADD = "int_add"
    INT_SUB = "int_sub"


class MathResult(BaseModel):
    operation: str
    a: int
    b: int
    result: int


class MathServer:
    def add(self, a: int, b: int) -> MathResult:
        """Perform integer addition"""
        return MathResult(
            operation="addition",
            a=a,
            b=b,
            result=a + b
        )

    def subtract(self, a: int, b: int) -> MathResult:
        """Perform integer subtraction"""
        return MathResult(
            operation="subtraction",
            a=a,
            b=b,
            result=a - b
        )


async def serve() -> None:
    server = Server("choumine-math")
    math_server = MathServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available math tools."""
        return [
            Tool(
                name=MathTools.INT_ADD.value,
                description="Perform integer addition",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer", "description": "First integer"},
                        "b": {"type": "integer", "description": "Second integer"},
                    },
                    "required": ["a", "b"],
                },
            ),
            Tool(
                name=MathTools.INT_SUB.value,
                description="Perform integer subtraction",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer", "description": "First integer"},
                        "b": {"type": "integer", "description": "Second integer"},
                    },
                    "required": ["a", "b"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent]:
        """Handle math tool calls."""
        try:
            match name:
                case MathTools.INT_ADD.value:
                    if not all(k in arguments for k in ["a", "b"]):
                        raise ValueError("Missing required arguments")
                    a = int(arguments["a"])
                    b = int(arguments["b"])
                    result = math_server.add(a, b)

                case MathTools.INT_SUB.value:
                    if not all(k in arguments for k in ["a", "b"]):
                        raise ValueError("Missing required arguments")
                    a = int(arguments["a"])
                    b = int(arguments["b"])
                    result = math_server.subtract(a, b)

                case _:
                    raise ValueError(f"Unknown tool: {name}")

            return [
                TextContent(
                    type="text", 
                    text=json.dumps(result.model_dump(), indent=2)
                )
            ]

        except Exception as e:
            raise ValueError(f"Error processing mcp-math query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)