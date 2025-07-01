import socket
import requests
import ipaddress
# def ports -- 21, 22, 23, 80, 443, 8080 for scanning grabs

def check_port(ip, port, timeout=0.5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

def scan_network(network_cidr, port=80, output=True):
    net = ipaddress.ip_network(network_cidr)
    alive_hosts = []
    for ip in net.hosts():
        ip_str = str(ip)
        if check_port(ip_str, port):
            print(f"[+] {ip_str}:{port} opened" if output else None)
            alive_hosts.append(ip_str)
        else:
            print(f"[-] {ip_str}:{port} closed" if output else None)
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
        return True  # Порт відкритий
    except (socket.timeout, ConnectionRefusedError):
        return False  # Порт закритий або недоступний
    except Exception as e:
        return False