#!/usr/bin/env python3
"""MCP Server for Blender."""

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server, stdio_server
from mcp.types import Tool, TextContent

from .blender_bridge import BlenderBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server("blender-mcp")
bridge = BlenderBridge()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Список инструментов MCP."""
    return [
        Tool(
            name="create_object",
            description="Создать 3D объект",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["cube", "sphere", "cylinder"]},
                    "location": {"type": "array", "items": {"type": "number"}},
                    "size": {"type": "number"}
                },
                "required": ["type"]
            }
        ),
        Tool(
            name="render_image",
            description="Рендерить изображение",
            inputSchema={
                "type": "object",
                "properties": {
                    "resolution_x": {"type": "integer"},
                    "resolution_y": {"type": "integer"},
                    "output_path": {"type": "string"}
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]):
    """Выполнить инструмент."""
    if name == "create_object":
        result = await bridge.create_object(**arguments)
    elif name == "render_image":
        result = await bridge.render_image(**arguments)
    else:
        result = {"error": f"Неизвестный инструмент: {name}"}
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    """Запуск сервера."""
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
