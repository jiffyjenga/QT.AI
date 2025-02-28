"""
Secure communications module for QT.AI trading bot.

This module provides functionality for secure communications using
HTTPS/WebSockets over TLS.
"""
import ssl
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SecureComms:
    """Secure communications using HTTPS/WebSockets over TLS."""
    
    def __init__(self, 
                 cert_file: Optional[str] = None,
                 key_file: Optional[str] = None,
                 ca_file: Optional[str] = None):
        """Initialize secure communications."""
        self.cert_file = cert_file
        self.key_file = key_file
        self.ca_file = ca_file
        self.ssl_context = None
        
        # Initialize SSL context
        self._initialize_ssl_context()
    
    def _initialize_ssl_context(self):
        """Initialize SSL context for secure communications."""
        try:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            
            if self.cert_file and self.key_file:
                self.ssl_context.load_cert_chain(self.cert_file, self.key_file)
            
            if self.ca_file:
                self.ssl_context.load_verify_locations(self.ca_file)
            
            # Set secure protocols and ciphers
            self.ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
            self.ssl_context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20')
            
            logger.info("SSL context initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing SSL context: {str(e)}")
            self.ssl_context = None
    
    def get_ssl_context(self) -> Optional[ssl.SSLContext]:
        """Get the SSL context for secure communications."""
        return self.ssl_context
    
    def get_websocket_ssl_context(self) -> Optional[ssl.SSLContext]:
        """Get the SSL context for WebSocket communications."""
        return self.ssl_context
