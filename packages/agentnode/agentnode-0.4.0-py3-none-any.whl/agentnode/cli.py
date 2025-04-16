#!/usr/bin/env python3
"""
AgentNode CLI

Main entry point for the AgentNode command-line interface.
"""

import argparse
import sys
import logging
import yaml
from typing import List, Optional, Dict, Any

from agentnode.launchers.network_launcher import launch_network
from agentnode.launchers.terminal_console import launch_console
from agentnode.agents.simple_openai_agent import SimpleOpenAIAgentRunner


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("agentnode.log")
        ]
    )


def launch_network_command(args: argparse.Namespace) -> None:
    """Handle launch-network command.
    
    Args:
        args: Command-line arguments
    """
    launch_network(args.config, args.runtime)


def connect_command(args: argparse.Namespace) -> None:
    """Handle connect command.
    
    Args:
        args: Command-line arguments
    """
    launch_console(args.ip, args.port, args.id)


def launch_agent_command(args: argparse.Namespace) -> None:
    """Handle launch-agent command.
    
    Args:
        args: Command-line arguments
    """
    # Load agent configuration from YAML file
    try:
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Failed to load agent configuration: {e}")
        return

    # Validate configuration
    if 'type' not in config:
        logging.error("Agent configuration must specify 'type'")
        return
    
    if 'config' not in config:
        logging.error("Agent configuration must include a 'config' section")
        return

    # Get the agent type and configuration
    agent_type = config['type']
    agent_config = config['config']
    
    # Create and launch the agent based on type
    try:
        # Check if the agent type is a fully qualified class path
        if '.' in agent_type:
            # Import the module and get the class
            module_path, class_name = agent_type.rsplit('.', 1)
            try:
                module = __import__(module_path, fromlist=[class_name])
                agent_class = getattr(module, class_name)
            except (ImportError, AttributeError) as e:
                logging.error(f"Failed to import agent class '{agent_type}': {e}")
                return
        else:
            # Handle predefined agent types
            if agent_type.lower() == 'openai':
                agent_class = SimpleOpenAIAgentRunner
            else:
                logging.error(f"Unsupported predefined agent type: {agent_type}")
                logging.info("Use a fully qualified class path (e.g., 'agentnode.agents.simple_openai_agent.SimpleOpenAIAgentRunner')")
                return
        
        # Create the agent using the config parameters directly as kwargs
        try:
            agent = agent_class(**agent_config)
            
            # Start the agent
            logging.info(f"Starting agent of type '{agent_type}' with ID '{agent_config.get('agent_id', 'unknown')}'")
            
            # Connection settings - prioritize command line arguments over config file
            host = args.host
            port = args.port
            network_id = args.network_id
            
            # If not provided in command line, try to get from config file
            if 'connection' in config:
                conn_config = config['connection']
                
                # Get host from config if not provided in command line
                if host is None:
                    host = conn_config.get('host')
                
                # Get port from config if not provided in command line
                if port is None:
                    port = conn_config.get('port')
                
                # Get network_id from config if not provided in command line
                if network_id is None:
                    # Support both network_id and network-id keys
                    network_id = conn_config.get('network_id') or conn_config.get('network-id')
            
            # Start the agent and wait for it to stop
            try:
                # Start the agent
                agent.start(
                    host=host,
                    port=port,
                    network_id=network_id,
                    metadata={"agent_type": agent_type}
                )
                
                # Wait for the agent to stop
                agent.wait_for_stop()
                
            except KeyboardInterrupt:
                logging.info("Agent stopped by user")
                agent.stop()
            except Exception as e:
                logging.error(f"Error running agent: {e}")
                agent.stop()
            
        except TypeError as e:
            logging.error(f"Error creating agent: {e}")
            logging.error("Check that your configuration parameters match the agent's constructor")
            return
        except Exception as e:
            logging.error(f"Unexpected error creating agent: {e}")
            return
    except Exception as e:
        logging.error(f"Failed to create agent: {e}")
        return


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        int: Exit code
    """
    parser = argparse.ArgumentParser(
        description="AgentNode - A flexible framework for building multi-agent systems"
    )
    parser.add_argument("--log-level", default="INFO", 
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Launch network command
    launch_network_parser = subparsers.add_parser("launch-network", help="Launch a network")
    launch_network_parser.add_argument("config", help="Path to network configuration file")
    launch_network_parser.add_argument("--runtime", type=int, help="Runtime in seconds (default: run indefinitely)")
    
    # Connect command
    connect_parser = subparsers.add_parser("connect", help="Connect to a network server")
    connect_parser.add_argument("--ip", required=True, help="Server IP address")
    connect_parser.add_argument("--port", type=int, default=8765, help="Server port (default: 8765)")
    connect_parser.add_argument("--id", help="Agent ID (default: auto-generated)")
    
    # Launch agent command
    launch_agent_parser = subparsers.add_parser("launch-agent", help="Launch an agent from a configuration file")
    launch_agent_parser.add_argument("config", help="Path to agent configuration file")
    launch_agent_parser.add_argument("--network-id", help="Network ID to connect to (overrides config file)")
    launch_agent_parser.add_argument("--host", help="Server host address (overrides config file)")
    launch_agent_parser.add_argument("--port", type=int, help="Server port (overrides config file)")
    
    # Parse arguments
    args = parser.parse_args(argv)
    
    # Set up logging
    setup_logging(args.log_level)
    
    try:
        if args.command == "launch-network":
            launch_network_command(args)
        elif args.command == "connect":
            connect_command(args)
        elif args.command == "launch-agent":
            launch_agent_command(args)
        else:
            parser.print_help()
            return 1
        
        return 0
    except Exception as e:
        logging.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 