"""
Service detection module for identifying services on open ports
"""

import socket
import threading
from config import COMMON_SERVICES


class ServiceDetector:
    """Detects services running on open ports"""

    def __init__(self, timeout=2):
        self.timeout = timeout

    def get_service_name(self, port):
        """Get service name from common services mapping"""
        return COMMON_SERVICES.get(port, 'Unknown')

    def identify_banner(self, host, port):
        """
        Try to identify service by connecting and reading banner
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, port))

            try:
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
                return banner if banner else self.get_service_name(port)
            except socket.timeout:
                sock.close()
                return self.get_service_name(port)
        except Exception as e:
            return self.get_service_name(port)

    def identify_service(self, host, port):
        """
        Identify service on a port using multiple methods
        """
        # First try to get from common services
        service = self.get_service_name(port)

        # Try to get banner for more detailed info
        banner = self.identify_banner(host, port)

        return {
            'port': port,
            'service': service,
            'banner': banner,
            'status': 'OPEN'
        }
