import asyncio
from scanner import get_local_ip, get_local_network, get_arp_devices, check_port

def main():
    devices = get_arp_devices()
    
    for ip in devices:
        for port in [22, 53, 80, 443, 445, 8080, 62078]:
            if check_port(ip, port):
                devices[ip]["ports"].append(port)
                print(f"{ip}:{port} -> open")
    print(f"\nDEVICES in the local network ({len(devices)}):")
    for ip in devices:
        print("---------------")
        print(f"{devices[ip]['name']}\nIP:{ip}\nMAC:{devices[ip]['mac']}\nAvailable ports:{devices[ip]['ports']}")



if __name__ == "__main__":
    main()
