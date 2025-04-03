"""Utility functions for the application."""
import socket
import logging

logger = logging.getLogger(__name__)

def find_available_port(start_port, max_attempts=100):
    """
    Find an available port starting from start_port.
    
    Args:
        start_port (int): The port to start checking from
        max_attempts (int): Maximum number of ports to check
        
    Returns:
        int: An available port, or the original port if none found
    """
    port = start_port
    for _ in range(max_attempts):
        try:
            # Try to create a socket and bind to the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(('127.0.0.1', port))
                # If we get here, the port is available
                return port
        except OSError:
            # Port is in use, try the next one
            logger.debug(f"Port {port} is in use, trying next port")
            port += 1
    
    # If we get here, we couldn't find an available port
    logger.warning(f"Could not find an available port after {max_attempts} attempts")
    return start_port  # Return the original port as a fallback
