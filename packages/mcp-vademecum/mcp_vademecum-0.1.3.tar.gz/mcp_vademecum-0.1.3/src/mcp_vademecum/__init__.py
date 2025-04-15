import argparse
from .server import mcp

def main():
    """MCP Vademecum"""
    parser = argparse.ArgumentParser(
        description="Tool para Vademecum."
    )
    parser.parse_args()
    mcp.run()

if __name__ == "__main__":
    main()