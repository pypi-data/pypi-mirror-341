# __init__.py

from .server import serve

def main():
    """MCP Math Server - Integer arithmetic operations for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="Provide integer addition and subtraction capabilities for models"
    )
    args = parser.parse_args()
    asyncio.run(serve())


if __name__ == "__main__":
    main()