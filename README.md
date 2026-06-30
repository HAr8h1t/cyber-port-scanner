# Cyber Port Scanner v2.0.0

A comprehensive, professional-grade port scanning tool with both CLI and GUI interfaces. Fast, multi-threaded scanning with service detection, customizable presets, and multiple export formats.

## Features

✨ **Core Features**
- 🚀 Multi-threaded port scanning for fast results
- 🎯 Customizable port ranges and presets
- 🔍 Service detection and banner grabbing
- 💾 Export results in TXT, CSV, or JSON formats
- 📊 Detailed scan statistics and history
- 🖥️ Interactive GUI interface with tkinter
- 💻 Command-line interface for automation
- ⚡ Configurable timeout and thread count

## System Requirements

- Python 3.6+
- tkinter (usually included with Python)
- No external dependencies required (only `requests` for potential enhancements)

## Installation

1. Clone the repository or extract the project files:
```bash
cd cyber-port-scanner
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode (Recommended)

Launch the graphical interface:
```bash
python main.py --gui
```

**GUI Features:**
- **Scanner Tab**: Configure target, port range, and options
- **Results Tab**: View detailed results with export options
- **History Tab**: Track all scans performed
- **About Tab**: Application information and warnings

### Command Line Mode

Basic scan on localhost:
```bash
python main.py
```

Scan a specific host:
```bash
python main.py -H 192.168.1.1
```

Scan specific port range:
```bash
python main.py -H example.com -s 1 -e 10000
```

Use a preset:
```bash
python main.py -H 192.168.1.1 --preset "Web Servers"
```

Export results:
```bash
python main.py -H 192.168.1.1 -e results.txt
python main.py -H 192.168.1.1 -e results.csv --export-format csv
python main.py -H 192.168.1.1 -e results.json --export-format json
```

Advanced options:
```bash
python main.py -H 192.168.1.1 -s 1 -e 65535 -t 1.0 --threads 100
```

### Command Line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--gui` | | Launch GUI interface |
| `--host` | `-H` | Target host (IP or hostname) |
| `--start-port` | `-s` | Start port number (default: 1) |
| `--end-port` | `-e` | End port number (default: 1024) |
| `--preset` | | Use preset port range |
| `--timeout` | `-t` | Socket timeout in seconds (default: 0.5) |
| `--threads` | | Maximum threads (default: 50) |
| `--export` | | Export results to file |
| `--export-format` | | Export format: txt, csv, json (default: txt) |
| `--version` | `-v` | Show version |

### Available Port Presets

- **Common Ports**: 1-1024
- **Web Servers**: 80, 443, 8080, 8443, 3000, 5000
- **Database Ports**: 3306, 5432, 27017, 6379, 1433
- **SSH/Telnet**: 22, 23, 3389
- **Mail Services**: 25, 110, 143, 465, 587, 993, 995
- **DNS**: 53
- **NTP**: 123
- **DHCP**: 67, 68
- **All Common**: 1-65535

## Project Structure

```
cyber-port-scanner/
├── main.py                 # Entry point with CLI interface
├── gui.py                  # GUI application using tkinter
├── scanner.py              # Core port scanning logic
├── service_detector.py     # Service identification module
├── config.py               # Configuration and constants
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore file
```

## File Descriptions

### main.py
Main entry point supporting both CLI and GUI modes. Handles command-line argument parsing and launches appropriate interface.

### gui.py
Interactive GUI application with four tabs:
- Scanner: Configure and run scans
- Results: View and export scan results
- History: Track scan history
- About: Application info

### scanner.py
Core scanning engine with:
- Multi-threaded port scanning
- Result aggregation
- Scan statistics
- Export functionality (TXT, CSV, JSON)

### service_detector.py
Service identification module providing:
- Port-to-service mapping
- Banner grabbing
- Service name lookup

### config.py
Configuration and constants including:
- Default parameters
- Port presets
- Service mappings
- Application settings

## Export Formats

### TXT Format
Human-readable summary with statistics and port details.

### CSV Format
Spreadsheet-compatible format with columns:
- Port, Service, Status, Banner

### JSON Format
Complete scan data including statistics and all results.

## Performance Tips

1. **Increase threads** for faster scans (use with caution on shared networks)
   ```bash
   python main.py -H 192.168.1.1 --threads 100
   ```

2. **Increase timeout** for unreliable networks
   ```bash
   python main.py -H 192.168.1.1 -t 2.0
   ```

3. **Reduce port range** to scan faster
   ```bash
   python main.py -H 192.168.1.1 -s 1 -e 1024
   ```

4. **Use presets** for quick scanning
   ```bash
   python main.py -H 192.168.1.1 --preset "Web Servers"
   ```

## Security & Legal Notice

⚠️ **WARNING**: Port scanning may be illegal in some jurisdictions. Only scan:
- Systems you own
- Systems you have explicit permission to scan
- Your own network

Unauthorized port scanning may violate laws including the Computer Fraud and Abuse Act (CFAA) in the US and similar laws in other countries.

The authors are not responsible for any misuse or damage caused by this tool.

## Troubleshooting

**Tkinter not found**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (with Homebrew)
brew install python-tk@3.x
```

**Permission denied (some systems)**
```bash
# Some privileged operations may require root
sudo python main.py -H target.com
```

**Scan seems slow**
- Increase `--threads` value
- Increase `--timeout` if network is unreliable
- Use smaller port ranges

## Examples

### Complete Workflow

1. Launch GUI:
   ```bash
   python main.py --gui
   ```

2. In GUI:
   - Enter target host
   - Select "Web Servers" preset
   - Adjust timeout if needed
   - Click "Start Scan"
   - View results in Results tab
   - Export to CSV

### Batch Scanning

```bash
# Scan multiple hosts
for host in 192.168.1.{1..10}; do
    python main.py -H $host -e scan_$host.txt
done
```

### Quick Security Check

```bash
python main.py -H 192.168.1.1 \
    --preset "Common Ports" \
    -e security_audit.json \
    --export-format json
```

## Version History

### v2.0.0 (Current)
- Added GUI interface
- Multi-threaded scanning
- Service detection
- Multiple export formats
- Scan history tracking
- Port presets
- Better error handling

### v1.0.0 (Original)
- Basic port scanning
- Simple CLI interface

## Contributing

Improvements and bug reports are welcome! Please ensure:
- Code follows PEP 8 style guide
- New features include proper documentation
- Test code before submitting

## License

This project is provided for educational and authorized security testing purposes only.

## Disclaimer

This tool is for educational purposes and authorized use only. Users are responsible for ensuring they have proper authorization before scanning any network or system. Unauthorized port scanning may be illegal.

---

**Questions or Issues?** Check the examples above or review the code documentation.

**Happy Scanning! 🔍**
