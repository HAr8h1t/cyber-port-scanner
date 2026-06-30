"""
Cyber Port Scanner - Main Entry Point
A comprehensive port scanning tool with CLI and GUI interfaces
"""

import argparse
import sys
from scanner import PortScanner
from config import APP_NAME, APP_VERSION, PORT_PRESETS


def print_banner():
    """Print application banner"""
    banner = f"""
    ╔═══════════════════════════════════╗
    ║   {APP_NAME}   ║
    ║       Version {APP_VERSION}            ║
    ╚═══════════════════════════════════╝
    """
    print(banner)


def scan_cli(args):
    """Command line scanning interface"""
    print_banner()

    print(f"[*] Target: {args.host}")
    print(f"[*] Port Range: {args.start_port} - {args.end_port}")
    print(f"[*] Timeout: {args.timeout}s")
    print()

    scanner = PortScanner(timeout=args.timeout, max_threads=args.threads)

    def progress_callback(event_type, data, extra):
        if event_type == 'port_found':
            print(f"[+] OPEN PORT: {data} ({extra})")
        elif event_type == 'scan_start':
            print(f"[*] Starting scan on {data}...")
        elif event_type == 'scan_complete':
            print("[*] Scan completed")

    scanner.set_callback(progress_callback)

    try:
        results = scanner.scan(args.host, args.start_port, args.end_port)

        print()
        print("=" * 50)
        print("SCAN RESULTS")
        print("=" * 50)

        stats = results['statistics']
        print(f"\nStatistics:")
        print(f"  Total Ports Scanned: {stats['total_ports']}")
        print(f"  Open Ports: {stats['open_count']}")
        print(f"  Closed Ports: {stats['closed_count']}")
        print(f"  Filtered Ports: {stats['filtered_count']}")
        print(f"  Scan Duration: {results['scan_time']}")

        if results['open_ports']:
            print(f"\nOpen Ports Found ({len(results['open_ports'])}):")
            print("-" * 50)
            for result in results['scan_results']:
                print(f"  Port {result['port']:5d} - {result['service']}")
        else:
            print("\n[!] No open ports found")

        # Export if requested
        if args.export:
            scanner.export_results(args.export, format=args.export_format)
            print(f"\n[+] Results exported to {args.export}")

    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)


def gui_interface():
    """Launch GUI interface"""
    from gui import main
    main()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description=f'{APP_NAME} v{APP_VERSION} - Fast Port Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan localhost with default ports
  python main.py

  # Scan a specific host
  python main.py -H 192.168.1.1

  # Scan specific port range
  python main.py -H example.com -s 1 -e 10000

  # Launch GUI interface
  python main.py --gui

  # Use quick preset
  python main.py -H 192.168.1.1 --preset "Web Servers"

  # Export results
  python main.py -H 192.168.1.1 -e scan_results.txt
        """
    )

    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch GUI interface'
    )

    parser.add_argument(
        '-H', '--host',
        default='127.0.0.1',
        help='Target host (IP or hostname) (default: 127.0.0.1)'
    )

    parser.add_argument(
        '-s', '--start-port',
        type=int,
        default=1,
        dest='start_port',
        help='Start port number (default: 1)'
    )

    parser.add_argument(
        '-e', '--end-port',
        type=int,
        default=1024,
        dest='end_port',
        help='End port number (default: 1024)'
    )

    parser.add_argument(
        '--preset',
        choices=list(PORT_PRESETS.keys()),
        help='Use preset port range'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=float,
        default=0.5,
        help='Socket timeout in seconds (default: 0.5)'
    )

    parser.add_argument(
        '--threads',
        type=int,
        default=50,
        help='Maximum number of threads (default: 50)'
    )

    parser.add_argument(
        '--export',
        metavar='FILENAME',
        help='Export results to file'
    )

    parser.add_argument(
        '--export-format',
        choices=['txt', 'csv', 'json'],
        default='txt',
        dest='export_format',
        help='Export file format (default: txt)'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'{APP_NAME} {APP_VERSION}'
    )

    args = parser.parse_args()

    # GUI mode
    if args.gui:
        try:
            gui_interface()
        except ImportError:
            print("[!] Tkinter not available. Using CLI mode instead.", file=sys.stderr)
            scan_cli(args)
        return

    # Apply preset if selected
    if args.preset:
        preset = PORT_PRESETS[args.preset]
        if isinstance(preset, tuple) and len(preset) == 2:
            args.start_port, args.end_port = preset

    # CLI scanning
    scan_cli(args)


if __name__ == '__main__':
    main()
