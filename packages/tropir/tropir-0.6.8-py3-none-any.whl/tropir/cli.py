"""
Command-line interface for the Tropir Agent.
"""

import os
import sys
import importlib.util
import runpy
import argparse
import re
from pathlib import Path

from . import initialize


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Tropir Agent CLI")
    parser.add_argument('command', help='Command to run with Tropir agent enabled')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the command')
    
    args = parser.parse_args()
    
    # Enable Tropir tracking
    os.environ["TROPIR_ENABLED"] = "1"
    
    # Try to load only TROPIR environment variables from .env file before initializing
    try:
        env_path = Path('.env')
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Look for TROPIR_API_KEY and TROPIR_API_URL specifically
                        if match := re.match(r'^(TROPIR_API_KEY|TROPIR_API_URL)\s*=\s*(.*)$', line):
                            key = match.group(1)
                            value = match.group(2).strip()
                            # Remove quotes if present
                            if (value[0] == value[-1] == '"' or value[0] == value[-1] == "'"):
                                value = value[1:-1]
                            os.environ[key] = value
    except Exception:
        pass
    
    # Initialize the agent
    initialize()
    
    # Add the current directory to the Python path
    sys.path.insert(0, os.getcwd())
    
    # Run the command
    if args.command == "python":
        if len(args.args) > 0:
            if args.args[0] == "-m":
                # Handle module execution
                if len(args.args) > 1:
                    module_name = args.args[1]
                    sys.argv = [args.args[0]] + args.args[1:]
                    try:
                        runpy.run_module(module_name, run_name="__main__")
                    except ModuleNotFoundError as e:
                        print(f"Error: {e}")
                        print("Make sure you're running this command from the correct directory.")
                        sys.exit(1)
                else:
                    print("Missing module name")
                    sys.exit(1)
            else:
                # Handle script execution
                script_path = args.args[0]
                sys.argv = args.args
                try:
                    runpy.run_path(script_path, run_name="__main__")
                except FileNotFoundError:
                    print(f"Error: File '{script_path}' not found.")
                    sys.exit(1)
        else:
            print("Missing python script or module")
            sys.exit(1)
    else:
        print(f"Unsupported command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main() 