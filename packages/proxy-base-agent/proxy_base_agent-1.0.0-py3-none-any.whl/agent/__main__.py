import asyncio
import logging
import os
import sys

from agent.interface.cli_interface import CLIInterface
from agent.system.setup_wizard import setup_agent

# Set up logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "WARNING"),
    format="[\033[1;33m%(levelname)s\033[0m] \033[34m%(message)s\033[0m",
    stream=sys.stdout,
)

async def main():
    """
    Initialize and run the agent with an interactive setup wizard.
    """
    # Create the interface
    interface = CLIInterface()
    agent = None

    try:
        # Run the setup wizard to configure and initialize the agent
        agent = await setup_agent(interface)
        # Start the agent loop
        await agent.loop()
    except Exception as error:
        # Handle any exceptions
        await interface.exit_program(error)
    finally:
        if agent:
            await agent.mcp_host.cleanup()

# Run the main function
try:
    asyncio.run(main())
except Exception as error:
    logging.error(f"Error: {error}")
    sys.exit(1)
