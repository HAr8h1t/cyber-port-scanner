"""
Core port scanning module
"""

import socket
import threading
import time
from datetime import datetime
from collections import defaultdict
from config import DEFAULT_TIMEOUT, DEFAULT_THREADS
from service_detector import ServiceDetector


class PortScanner:
    """Main port scanner class"""

    def __init__(self, timeout=DEFAULT_TIMEOUT, max_threads=DEFAULT_THREADS):
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []
        self.scan_results = []
        self.is_scanning = False
        self.scan_stats = {
            'start_time': None,
            'end_time': None,
            'total_ports': 0,
            'open_count': 0,
            'closed_count': 0,
            'filtered_count': 0,
        }
        self.service_detector = ServiceDetector()
        self.lock = threading.Lock()
        self.callback = None

    def set_callback(self, callback):
        """Set callback function for progress updates"""
        self.callback = callback

    def _scan_port(self, host, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)

            result = sock.connect_ex((host, port))

            if result == 0:
                service_info = self.service_detector.identify_service(host, port)
                with self.lock:
                    self.open_ports.append(port)
                    self.scan_results.append(service_info)
                    self.scan_stats['open_count'] += 1

                if self.callback:
                    self.callback('port_found', port, service_info['service'])

            else:
                with self.lock:
                    self.closed_ports.append(port)
                    self.scan_stats['closed_count'] += 1

            sock.close()

        except socket.timeout:
            with self.lock:
                self.filtered_ports.append(port)
                self.scan_stats['filtered_count'] += 1
        except Exception as e:
            with self.lock:
                self.closed_ports.append(port)

        if self.callback:
            self.callback('port_checked', port, None)

    def scan(self, host, start_port, end_port, custom_ports=None):
        """
        Scan ports on the given host
        
        Args:
            host: Target host IP or hostname
            start_port: Starting port number
            end_port: Ending port number
            custom_ports: List of specific ports to scan instead of range
        """
        self.is_scanning = True
        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []
        self.scan_results = []

        # Validate and resolve host
        try:
            host_ip = socket.gethostbyname(host)
        except socket.gaierror:
            raise Exception(f"Hostname {host} cannot be resolved")
        except socket.error:
            raise Exception(f"Could not connect to host {host}")

        # Determine ports to scan
        if custom_ports:
            ports_to_scan = custom_ports
        else:
            ports_to_scan = list(range(start_port, end_port + 1))

        self.scan_stats['start_time'] = datetime.now()
        self.scan_stats['total_ports'] = len(ports_to_scan)

        if self.callback:
            self.callback('scan_start', host_ip, len(ports_to_scan))

        # Use threading for faster scanning
        threads = []
        for port in ports_to_scan:
            if not self.is_scanning:
                break

            while len(threading.enumerate()) > self.max_threads:
                time.sleep(0.1)

            thread = threading.Thread(target=self._scan_port, args=(host_ip, port))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        self.scan_stats['end_time'] = datetime.now()
        self.is_scanning = False

        if self.callback:
            self.callback('scan_complete', None, None)

        return self.get_results()

    def get_results(self):
        """Get scan results"""
        return {
            'open_ports': sorted(self.open_ports),
            'scan_results': sorted(self.scan_results, key=lambda x: x['port']),
            'statistics': self.scan_stats,
            'scan_time': self._get_scan_duration()
        }

    def _get_scan_duration(self):
        """Calculate scan duration"""
        if self.scan_stats['start_time'] and self.scan_stats['end_time']:
            delta = self.scan_stats['end_time'] - self.scan_stats['start_time']
            return str(delta).split('.')[0]
        return "0:00:00"

    def stop_scan(self):
        """Stop the ongoing scan"""
        self.is_scanning = False

    def export_results(self, filename, format='txt'):
        """Export scan results to file"""
        if format == 'txt':
            self._export_txt(filename)
        elif format == 'csv':
            self._export_csv(filename)
        elif format == 'json':
            self._export_json(filename)

    def _export_txt(self, filename):
        """Export results as text file"""
        with open(filename, 'w') as f:
            f.write(f"Cyber Port Scanner Results\n")
            f.write(f"{'=' * 50}\n\n")
            f.write(f"Scan Time: {self.scan_stats['start_time']}\n")
            f.write(f"Duration: {self._get_scan_duration()}\n")
            f.write(f"Total Ports Scanned: {self.scan_stats['total_ports']}\n\n")

            f.write(f"Statistics:\n")
            f.write(f"  Open Ports: {self.scan_stats['open_count']}\n")
            f.write(f"  Closed Ports: {self.scan_stats['closed_count']}\n")
            f.write(f"  Filtered Ports: {self.scan_stats['filtered_count']}\n\n")

            if self.scan_results:
                f.write(f"Open Ports Details:\n")
                f.write(f"{'-' * 50}\n")
                for result in self.scan_results:
                    f.write(f"Port {result['port']}: {result['service']}\n")
            else:
                f.write("No open ports found.\n")

    def _export_csv(self, filename):
        """Export results as CSV file"""
        import csv
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Port', 'Service', 'Status', 'Banner'])
            for result in self.scan_results:
                writer.writerow([
                    result['port'],
                    result['service'],
                    result['status'],
                    result.get('banner', '')
                ])

    def _export_json(self, filename):
        """Export results as JSON file"""
        import json
        with open(filename, 'w') as f:
            json.dump(self.get_results(), f, indent=2, default=str)

