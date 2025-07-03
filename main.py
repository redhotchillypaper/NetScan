import ipaddress
import socket
import ip_config as ipc
import beauty
import asyncio




async def main():
    results = await beauty.b_asyncscan_localnetwork()  
    results = [(ip, ports) for ip, ports in results if ports]
    banners = await beauty.b_asyncgrab_banners(results)
    useful_banners = [banner for banner in banners if ipc.is_banner_useful(banner)]
    print("\n\n\n\n\n\n")
    for each in useful_banners:
        print(f"{'-'*30}")
        print(each)
    print(useful_banners[0])





if __name__ == "__main__":
    asyncio.run(main())





# from scapy.all import ARP, Ether, srp

# def arp_scan(network_cidr):
#     # Створюємо ARP-запит і обгортку Ethernet
#     arp = ARP(pdst=network_cidr)
#     ether = Ether(dst="ff:ff:ff:ff:ff:ff")
#     packet = ether/arp

#     # Відправляємо пакет у мережу і отримуємо відповіді
#     result = srp(packet, timeout=3, verbose=0)[0]

#     # Парсимо відповіді
#     devices = []
#     for sent, received in result:
#         devices.append({'ip': received.psrc, 'mac': received.hwsrc})

#     return devices

# if __name__ == "__main__":
#     network = "192.168.68.0/24"
#     devices = arp_scan(network)
#     print("Devices found:")
#     for device in devices:
#         print(f"IP: {device['ip']}  MAC: {device['mac']}")


