import os
import argparse
import logging
from app import create_app
from app.utils import find_available_port
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Run the Flask application')
    parser.add_argument('--config', '-c',
                        default=os.getenv('FLASK_CONFIG', 'default'),
                        help='Configuration to use (default: from FLASK_CONFIG env var or "default")')
    parser.add_argument('--host', '-H',
                        help='Host to bind to (default: from config)')
    parser.add_argument('--port', '-p', type=int,
                        help='Port to bind to (default: from config)')
    parser.add_argument('--auto-port', '-a', action='store_true',
                        help='Automatically find an available port if the specified one is in use')
    parser.add_argument('--instance-name', '-i',
                        default=os.getenv('FLASK_INSTANCE', ''),
                        help='Instance name for running multiple instances (default: from FLASK_INSTANCE env var)')
    return parser.parse_args()

# Get configuration name from environment or command line
args = parse_args()
config_name = args.config
instance_name = args.instance_name

# Create the Flask application
app = create_app(config_name)

# Get the appropriate configuration class
config_class = config[config_name]

# Determine host and port
host = args.host or config_class.SERVER_HOST
base_port = args.port or config_class.SERVER_PORT

# If instance name is provided, modify the port
if instance_name:
    # Add a hash of the instance name to the port to make it unique
    # This ensures the same instance name always gets the same port offset
    port_offset = hash(instance_name) % 1000  # Keep the offset reasonable
    port = base_port + port_offset
    logger.info(f"Instance '{instance_name}' using port offset {port_offset} (port {port})")
else:
    port = base_port

# Find an available port if requested
if args.auto_port:
    original_port = port
    port = find_available_port(port)
    if port != original_port:
        logger.info(f"Port {original_port} was in use, using port {port} instead")

if __name__ == '__main__':
    logger.info(f"Starting {config_name} server on {host}:{port}")

    # Use the host and port from the configuration or command line
    app.run(
        host=host,
        port=port,
        debug=getattr(config_class, 'DEBUG', False)
    )
