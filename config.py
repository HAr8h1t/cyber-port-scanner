"""
Configuration settings for Cyber Port Scanner
"""

# Default scanning parameters
DEFAULT_TIMEOUT = 0.5  # seconds
DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 1024
DEFAULT_THREADS = 50

# Common port presets
PORT_PRESETS = {
    'Common Ports': (1, 1024),
    'Web Servers': (80, 443, 8080, 8443, 3000, 5000),
    'Database Ports': (3306, 5432, 27017, 6379, 1433),
    'SSH/Telnet': (22, 23, 3389),
    'Mail Services': (25, 110, 143, 465, 587, 993, 995),
    'DNS': (53,),
    'NTP': (123,),
    'DHCP': (67, 68),
    'All Common': (1, 65535),
}

# Service names for common ports
COMMON_SERVICES = {
    20: 'FTP-DATA',
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    67: 'DHCP',
    68: 'DHCP',
    69: 'TFTP',
    80: 'HTTP',
    110: 'POP3',
    123: 'NTP',
    135: 'RPC',
    139: 'NetBIOS',
    143: 'IMAP',
    161: 'SNMP',
    162: 'SNMP-Trap',
    389: 'LDAP',
    443: 'HTTPS',
    445: 'SMB',
    465: 'SMTPS',
    514: 'Syslog',
    587: 'SMTP',
    636: 'LDAPS',
    993: 'IMAPS',
    995: 'POP3S',
    1433: 'MSSQL',
    3306: 'MySQL',
    3389: 'RDP',
    5432: 'PostgreSQL',
    5900: 'VNC',
    6379: 'Redis',
    8080: 'HTTP-Alt',
    8443: 'HTTPS-Alt',
    27017: 'MongoDB',
}

# Application settings
APP_NAME = 'Cyber Port Scanner'
APP_VERSION = '2.0.0'
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
