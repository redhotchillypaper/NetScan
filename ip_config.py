import socket
import requests
import ipaddress
import asyncio
import subprocess
import platform



PORTS = [21, 22, 23, 25, 65, 66, 67, 80, 443, 5555, 8080, 62078]
useful_keywords = [
    "http/", "html", "<html", "<!doctype", "server:", "apache", "nginx", "tp-link", "mikrotik", "camera",
    "router", "meta http-equiv", "login", "admin", "welcome"
]

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
        return True  # Порт відкритий
    except (socket.timeout, ConnectionRefusedError):
        return False  # Порт закритий або недоступний
    except Exception as e:
        return False
    


async def async_grab_banner(ip, port, timeout=3):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )

        writer.write(b"GET / HTTP/1.0\r\n\r\n")
        await writer.drain()

        banner = b""
        while True:
            chunk = await asyncio.wait_for(reader.read(1024), timeout=timeout)
            if not chunk:
                break
            banner += chunk

        writer.close()
        await writer.wait_closed()

        return banner.decode(errors="ignore")

    except asyncio.TimeoutError:
        return f"Timeout on {ip}:{port}"
    except Exception as e:
        return f"Error on {ip}:{port}: {e}"



# banner filters 
def is_banner_useful(banner):
    banner = banner.lower().split(" ")
    for word in useful_keywords:
        if word in banner:
            return True

        
    return False

def analyze_banner(banner):
    banner = banner.lower()
    banner_info = {"service":"unknown","version":"unknown","info":""}
    if "http/" in banner:
        banner_info["service"] = "http"
        if "server:" in banner:
            start = banner.find("server:") + len("server:")
            end = banner.find("\n", start)
            banner_info["version"] = banner[start:end].strip()
    elif banner.startswith("ssh-"):
        banner_info["service"] = "ssh"
        banner_info["version"] = banner.strip()
    elif banner.startswith("220") and "ftp" in banner:
        banner_info["service"] = "ftp"
        banner_info["version"] = banner.strip()
    elif banner.startswith("220") and "smtp" in banner:
        banner_info["service"] = "smtp"
        banner_info["version"] = banner.strip()

    banner_info["info"] = banner.strip()[:200]  # перші 200 символів
    return banner_info



# getting asynchronous func
async def async_check_port(ip, port, timeout=2):
    try:
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False

async def async_scan_ip(ip, ports):
    open_ports = []
    tasks = [async_check_port(ip, port) for port in ports]
    results = await asyncio.gather(*tasks)

    for port, is_open in zip(ports, results):
        if is_open:
            open_ports.append(port)
    return ip, open_ports

async def scan_network_async(network_cidr, ports=PORTS):
    try:
        network = ipaddress.ip_network(network_cidr, strict=False)
    except Exception as e:
        print(f"Invalid network: {e}")
        return []

    tasks = [async_scan_ip(str(ip), ports) for ip in network.hosts()]
    return await asyncio.gather(*tasks)
