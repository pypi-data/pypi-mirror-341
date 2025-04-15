"""
Command execution for FastJango management commands.
"""

import os
import sys
import importlib
from typing import List, Optional

from fastjango.core.logging import Logger, setup_logging

# Setup logger
logger = Logger("fastjango.core.management")


def execute_from_command_line(argv: Optional[List[str]] = None) -> None:
    """
    Execute a command from the command line.
    
    Args:
        argv: Command line arguments (defaults to sys.argv)
    """
    # Setup logging
    setup_logging()
    
    # Get command line arguments
    if argv is None:
        argv = sys.argv
    
    # Parse command
    if len(argv) > 1:
        command = argv[1]
    else:
        # No command provided, show help
        command = "help"
    
    # Execute command
    try:
        if command == "help":
            show_help()
        elif command == "runserver":
            run_server(argv[2:])
        elif command == "startapp":
            start_app(argv[2:])
        elif command == "shell":
            run_shell()
        elif command == "migrate":
            run_migrate(argv[2:])
        elif command == "makemigrations":
            make_migrations(argv[2:])
        else:
            # Try to find a custom command
            try:
                run_custom_command(command, argv[2:])
            except ImportError:
                logger.error(f"Unknown command: {command}")
                show_help()
                sys.exit(1)
    except Exception as e:
        logger.error(f"Error executing command: {e}", exc_info=True)
        sys.exit(1)


def show_help() -> None:
    """Show help for available commands."""
    print("Available commands:")
    print("  runserver - Run the development server")
    print("  startapp - Create a new app")
    print("  shell - Run a Python shell")
    print("  migrate - Apply database migrations")
    print("  makemigrations - Create new migrations")
    print("  help - Show this help message")


def run_server(args: List[str]) -> None:
    """
    Run the development server.
    
    Args:
        args: Command line arguments
    """
    from fastjango.cli.commands.runserver import run_server as run_dev_server
    
    # Parse arguments
    host = "127.0.0.1"
    port = 8000
    reload = True
    
    # Parse host and port from args
    for arg in args:
        if arg.startswith("--host="):
            host = arg.split("=")[1]
        elif arg.startswith("--port="):
            port = int(arg.split("=")[1])
        elif arg == "--noreload":
            reload = False
    
    # Run server
    run_dev_server(host, port, reload)


def start_app(args: List[str]) -> None:
    """
    Create a new app.
    
    Args:
        args: Command line arguments
    """
    from pathlib import Path
    from fastjango.cli.commands.startapp import create_app
    
    if not args:
        logger.error("App name is required")
        print("Usage: manage.py startapp <app_name>")
        sys.exit(1)
    
    app_name = args[0]
    target_dir = Path(os.getcwd())
    
    create_app(app_name, target_dir)


def run_shell() -> None:
    """Run a Python shell with the FastJango environment."""
    try:
        # Try to use IPython if available
        import IPython
        from traitlets.config import Config
        
        # Configure IPython
        c = Config()
        c.InteractiveShellApp.exec_lines = [
            "import os",
            "import sys",
            "import importlib",
            "from pathlib import Path",
            "from fastjango.core.management import execute_from_command_line",
            "print('FastJango shell. Type \"help\" for more information.')",
        ]
        
        # Start IPython
        IPython.start_ipython(argv=[], config=c)
    except ImportError:
        # Fall back to standard Python shell
        import code
        
        # Create local variables
        locals_dict = {
            "os": os,
            "sys": sys,
            "importlib": importlib,
            "Path": __import__("pathlib").Path,
            "execute_from_command_line": execute_from_command_line,
        }
        
        # Print banner
        print("FastJango shell. Type \"help\" for more information.")
        
        # Start interactive console
        code.interact(local=locals_dict)


def run_migrate(args: List[str]) -> None:
    """
    Apply database migrations.
    
    Args:
        args: Command line arguments
    """
    # This is a placeholder for actual migration logic
    # In a real implementation, you would use SQLAlchemy/Alembic
    logger.info("Applying database migrations...")
    logger.info("Migrations applied successfully")


def make_migrations(args: List[str]) -> None:
    """
    Create new database migrations.
    
    Args:
        args: Command line arguments
    """
    # This is a placeholder for actual migration creation logic
    # In a real implementation, you would use SQLAlchemy/Alembic
    logger.info("Creating database migrations...")
    logger.info("Migrations created successfully")


def run_custom_command(command: str, args: List[str]) -> None:
    """
    Run a custom command from an app.
    
    Args:
        command: The command name
        args: Command line arguments
        
    Raises:
        ImportError: If the command module could not be found
    """
    # Get settings module
    settings_module = os.environ.get("FASTJANGO_SETTINGS_MODULE")
    if not settings_module:
        raise ImportError("Settings module not found")
    
    # Import settings
    settings = importlib.import_module(settings_module)
    
    # Look for command in installed apps
    installed_apps = getattr(settings, "INSTALLED_APPS", [])
    
    for app in installed_apps:
        try:
            # Try to import the command module
            command_module = f"{app}.management.commands.{command}"
            module = importlib.import_module(command_module)
            
            # Execute command
            if hasattr(module, "Command"):
                cmd = module.Command()
                cmd.execute(*args)
                return
        except ImportError:
            # Command not found in this app, continue to next app
            continue
    
    # If we get here, command was not found
    raise ImportError(f"Command '{command}' not found in any installed app") 