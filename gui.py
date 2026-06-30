"""
GUI interface for Cyber Port Scanner using tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
from scanner import PortScanner
from config import (
    PORT_PRESETS, COMMON_SERVICES, APP_NAME, APP_VERSION,
    WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_START_PORT, DEFAULT_END_PORT
)


class PortScannerGUI:
    """GUI application for port scanning"""

    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.scanner = PortScanner()
        self.scanner.set_callback(self.update_progress)
        self.scan_thread = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Scan
        self.scan_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.scan_tab, text='Scanner')
        self.setup_scan_tab()

        # Tab 2: Results
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text='Results')
        self.setup_results_tab()

        # Tab 3: History
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text='History')
        self.setup_history_tab()

        # Tab 4: About
        self.about_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.about_tab, text='About')
        self.setup_about_tab()

    def setup_scan_tab(self):
        """Setup scan tab"""
        # Main frame
        main_frame = ttk.Frame(self.scan_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Host frame
        host_frame = ttk.LabelFrame(main_frame, text="Target Host", padding="10")
        host_frame.pack(fill=tk.X, pady=5)

        ttk.Label(host_frame, text="Host (IP or Hostname):").pack(side=tk.LEFT, padx=5)
        self.host_entry = ttk.Entry(host_frame, width=30)
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.pack(side=tk.LEFT, padx=5)

        # Port range frame
        port_frame = ttk.LabelFrame(main_frame, text="Port Range", padding="10")
        port_frame.pack(fill=tk.X, pady=5)

        ttk.Label(port_frame, text="Start Port:").grid(row=0, column=0, padx=5)
        self.start_port = ttk.Spinbox(port_frame, from_=1, to=65535, width=10)
        self.start_port.set(DEFAULT_START_PORT)
        self.start_port.grid(row=0, column=1, padx=5)

        ttk.Label(port_frame, text="End Port:").grid(row=0, column=2, padx=5)
        self.end_port = ttk.Spinbox(port_frame, from_=1, to=65535, width=10)
        self.end_port.set(DEFAULT_END_PORT)
        self.end_port.grid(row=0, column=3, padx=5)

        # Port presets
        ttk.Label(port_frame, text="Quick Presets:").grid(row=1, column=0, padx=5, pady=5)
        self.preset_var = tk.StringVar(value="Common Ports")
        preset_menu = ttk.Combobox(
            port_frame, textvariable=self.preset_var,
            values=list(PORT_PRESETS.keys()), state='readonly', width=20
        )
        preset_menu.grid(row=1, column=1, columnspan=2, padx=5)
        preset_menu.bind('<<ComboboxSelected>>', self.apply_preset)

        # Custom ports frame
        custom_frame = ttk.LabelFrame(main_frame, text="Custom Ports", padding="10")
        custom_frame.pack(fill=tk.X, pady=5)

        ttk.Label(custom_frame, text="Enter ports (comma-separated):").pack(anchor=tk.W)
        self.custom_ports = ttk.Entry(custom_frame, width=50)
        self.custom_ports.pack(fill=tk.X, pady=5)
        ttk.Label(
            custom_frame,
            text="Example: 22,80,443,3306,5432",
            foreground="gray"
        ).pack(anchor=tk.W)

        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=5)

        ttk.Label(options_frame, text="Timeout (seconds):").pack(side=tk.LEFT, padx=5)
        self.timeout = ttk.Spinbox(options_frame, from_=0.1, to=10, width=5)
        self.timeout.set(0.5)
        self.timeout.pack(side=tk.LEFT, padx=5)

        ttk.Label(options_frame, text="Max Threads:").pack(side=tk.LEFT, padx=5)
        self.threads = ttk.Spinbox(options_frame, from_=1, to=200, width=5)
        self.threads.set(50)
        self.threads.pack(side=tk.LEFT, padx=5)

        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.X, pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=5)

        self.status_label = ttk.Label(progress_frame, text="Ready", foreground="green")
        self.status_label.pack(anchor=tk.W)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.scan_button = ttk.Button(
            button_frame, text="Start Scan", command=self.start_scan
        )
        self.scan_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(
            button_frame, text="Stop Scan", command=self.stop_scan, state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Clear", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)

    def setup_results_tab(self):
        """Setup results tab"""
        main_frame = ttk.Frame(self.results_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)

        self.stats_text = tk.StringVar(value="No scan results yet")
        stats_label = ttk.Label(stats_frame, textvariable=self.stats_text, justify=tk.LEFT)
        stats_label.pack(anchor=tk.W)

        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Open Ports", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Create treeview for results
        self.results_tree = ttk.Treeview(
            results_frame, columns=('Port', 'Service', 'Status'), height=15
        )
        self.results_tree.column('#0', width=0, stretch=tk.NO)
        self.results_tree.column('Port', anchor=tk.W, width=100)
        self.results_tree.column('Service', anchor=tk.W, width=200)
        self.results_tree.column('Status', anchor=tk.W, width=100)

        self.results_tree.heading('#0', text='', anchor=tk.W)
        self.results_tree.heading('Port', text='Port', anchor=tk.W)
        self.results_tree.heading('Service', text='Service', anchor=tk.W)
        self.results_tree.heading('Status', text='Status', anchor=tk.W)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)

        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Export buttons frame
        export_frame = ttk.Frame(main_frame)
        export_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            export_frame, text="Export as TXT", command=lambda: self.export_results('txt')
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            export_frame, text="Export as CSV", command=lambda: self.export_results('csv')
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            export_frame, text="Export as JSON", command=lambda: self.export_results('json')
        ).pack(side=tk.LEFT, padx=5)

    def setup_history_tab(self):
        """Setup history tab"""
        main_frame = ttk.Frame(self.history_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Scan History", font=("Arial", 12, "bold")).pack(anchor=tk.W)

        self.history_text = scrolledtext.ScrolledText(
            main_frame, height=20, width=80, state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def setup_about_tab(self):
        """Setup about tab"""
        main_frame = ttk.Frame(self.about_tab, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        about_text = f"""
{APP_NAME} v{APP_VERSION}

A comprehensive port scanning tool with GUI interface.

Features:
• Fast multi-threaded port scanning
• Service detection and banner grabbing
• Customizable port ranges and presets
• Export results (TXT, CSV, JSON)
• Scan history tracking
• Detailed statistics

Usage:
1. Enter target host (IP or hostname)
2. Select port range or use quick presets
3. Configure scanning options
4. Click "Start Scan"
5. View results and export if needed

Supported Ports:
Common services for ports 1-65535 are recognized.

Warning:
Only scan networks and systems you own or have 
explicit permission to scan. Unauthorized port 
scanning may be illegal.

Version: {APP_VERSION}
"""

        about_label = ttk.Label(main_frame, text=about_text, justify=tk.LEFT)
        about_label.pack(anchor=tk.W)

    def apply_preset(self, event=None):
        """Apply port range preset"""
        preset_name = self.preset_var.get()
        preset = PORT_PRESETS.get(preset_name)

        if isinstance(preset, tuple) and len(preset) == 2:
            self.start_port.set(preset[0])
            self.end_port.set(preset[1])
        elif isinstance(preset, tuple):
            self.custom_ports.delete(0, tk.END)
            self.custom_ports.insert(0, ','.join(map(str, preset)))

    def start_scan(self):
        """Start port scanning"""
        host = self.host_entry.get().strip()
        if not host:
            messagebox.showerror("Error", "Please enter a host")
            return

        custom_ports_str = self.custom_ports.get().strip()
        if custom_ports_str:
            try:
                custom_ports = [int(p.strip()) for p in custom_ports_str.split(',')]
                start_port, end_port = None, None
            except ValueError:
                messagebox.showerror("Error", "Invalid custom ports format")
                return
        else:
            try:
                start_port = int(self.start_port.get())
                end_port = int(self.end_port.get())
                custom_ports = None
            except ValueError:
                messagebox.showerror("Error", "Invalid port numbers")
                return

        timeout = float(self.timeout.get())
        max_threads = int(self.threads.get())

        self.scanner = PortScanner(timeout=timeout, max_threads=max_threads)
        self.scanner.set_callback(self.update_progress)

        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Scanning...", foreground="blue")

        self.scan_thread = threading.Thread(
            target=self._scan_worker,
            args=(host, start_port, end_port, custom_ports)
        )
        self.scan_thread.daemon = True
        self.scan_thread.start()

    def _scan_worker(self, host, start_port, end_port, custom_ports):
        """Worker thread for scanning"""
        try:
            results = self.scanner.scan(host, start_port, end_port, custom_ports)
            self.root.after(0, self.display_results, results)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", str(e)))
            self.root.after(0, self.scan_complete)

    def update_progress(self, event_type, data, extra):
        """Update progress callback"""
        if event_type == 'scan_start':
            self.progress_var.set(0)
        elif event_type == 'port_checked':
            current = self.progress_var.get()
            self.progress_var.set(current + 1)
        elif event_type == 'port_found':
            self.status_label.config(
                text=f"Found: {data} ({extra})",
                foreground="green"
            )

    def display_results(self, results):
        """Display scan results"""
        self.results_tree.delete(*self.results_tree.get_children())

        for result in results['scan_results']:
            self.results_tree.insert(
                '',
                'end',
                values=(
                    result['port'],
                    result['service'],
                    result['status']
                )
            )

        stats = results['statistics']
        stats_text = (
            f"Total Ports: {stats['total_ports']}\n"
            f"Open Ports: {stats['open_count']}\n"
            f"Closed Ports: {stats['closed_count']}\n"
            f"Filtered Ports: {stats['filtered_count']}\n"
            f"Scan Duration: {results['scan_time']}"
        )
        self.stats_text.set(stats_text)

        self.update_history(results)
        self.scan_complete()

    def update_history(self, results):
        """Update scan history"""
        self.history_text.config(state=tk.NORMAL)
        history_entry = f"Scan completed: {results['statistics']['start_time']}\n"
        history_entry += f"Open ports: {', '.join(map(str, results['open_ports'])) or 'None'}\n"
        history_entry += "-" * 80 + "\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

    def stop_scan(self):
        """Stop scanning"""
        self.scanner.stop_scan()
        self.scan_complete()

    def scan_complete(self):
        """Scan completed"""
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Ready", foreground="green")
        self.progress_var.set(0)

    def export_results(self, format_type):
        """Export results to file"""
        if not self.scanner.scan_results:
            messagebox.showwarning("No Results", "No scan results to export")
            return

        file_types = {
            'txt': ('Text files', '*.txt'),
            'csv': ('CSV files', '*.csv'),
            'json': ('JSON files', '*.json'),
        }

        filename = filedialog.asksaveasfilename(
            defaultextension=f'.{format_type}',
            filetypes=[file_types[format_type], ('All files', '*.*')]
        )

        if filename:
            try:
                self.scanner.export_results(filename, format_type)
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def clear_inputs(self):
        """Clear all input fields"""
        self.host_entry.delete(0, tk.END)
        self.host_entry.insert(0, "127.0.0.1")
        self.start_port.set(1)
        self.end_port.set(1024)
        self.custom_ports.delete(0, tk.END)
        self.timeout.set(0.5)
        self.threads.set(50)


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
