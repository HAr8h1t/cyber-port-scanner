# CONFLICT BRANCH VERSION
import socket

target = "127.0.0.1"
start_port = 20
end_port = 1024

per=input("Do you want to start scanning(y/n): ")
if per=="y":
    print(f"\nScanning {target} from port {start_port} to {end_port}\n")
else:
    print("lol still going to do")
    print(f"\nScanning {target} from port {start_port} to {end_port}\n")

open_ports = []

for port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)

    try:
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"[OPEN] Port {port}")
            open_ports.append(port)
    except KeyboardInterrupt:
        print("\nScan stopped by user.")
        break
    except Exception:
        pass
    finally:
        s.close()

print("\nScan complete.")

if open_ports:
    print("Open ports found:", open_ports)
else:
    print("No open ports found.")

