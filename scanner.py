import subprocess
import re
import socket
import requests
import ipaddress
import subprocess
import platform
from scapy.all import ARP, Ether, srp


PORTS = [22, 53, 80, 443, 445, 8080, 62078]
useful_keywords = [
    "http/", "html", "<html", "<!doctype", "server:", "apache", "nginx", "tp-link", "mikrotik", "camera",
    "router", "meta http-equiv", "login", "admin", "welcome"
]


# port checking
def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def check_port(ip, port, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

def scan_network(network_cidr, port=80, output=False):
    net = ipaddress.ip_network(network_cidr)
    alive_hosts = []
    for ip in net.hosts():
        ip_str = str(ip)
        if check_port(ip_str, port):
            print(f"[+] {ip_str}:{port}\topened" if output else None)
            alive_hosts.append(ip_str)
        else:
            print(f"[-] {ip_str}:{port}\tclosed" if output else None)
    return alive_hosts

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_local_network(ip, netmask="255.255.255.0"):
    interface = ipaddress.IPv4Interface(f"{ip}/{netmask}")
    return str(interface.network)

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=5)
        return response.text
    except Exception as e:
        return f"Public IP is not available at the moment: {e}"

def check_port(ip, port, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True  # Open
    except (socket.timeout, ConnectionRefusedError):
        return False  # closed
    except Exception as e:
        return False

# ARP scan


def get_arp_devices():
    """
    Reads local ARP table and returns active devices only.
    Works well on macOS/Linux.
    """
    try:
        output = subprocess.check_output(["arp", "-a"], text=True)
    except Exception as e:
        print(f"ARP lookup failed: {e}")
        return []

    devices = {}

    for line in output.splitlines():
        # ignore incomplete entries
        if "(incomplete)" in line:
            continue

        match = re.search(
            r"(?P<name>.*?)\s+\((?P<ip>\d+\.\d+\.\d+\.\d+)\)\s+at\s+(?P<mac>[0-9a-fA-F:]+)",
            line
        )

        if match:
            devices[match.group("ip")] = {
                "name": match.group("name").strip(),
                "mac": match.group("mac").lower(),
                "ports": []
            }

    return devices


def generate_report():
    devices = get_arp_devices()
    report = []
    report.append("OPEN IPS:PORTS:")
    for ip in devices:
        for port in PORTS:
            if check_port(ip, port):
                devices[ip]["ports"].append(port)
                report.append(f"{ip}:{port} -> open")
    report.append(f"\nDEVICES in the local network ({len(devices)}):")
    for ip in devices:
        report.append("---------------")
        report.append(f"{devices[ip]['name']}\nIP:{ip}\nMAC:{devices[ip]['mac']}\nAvailable ports:{devices[ip]['ports']}")

    return "\n".join(report)