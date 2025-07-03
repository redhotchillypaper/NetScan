import ip_config
import asyncio

async def b_asyncscan_localnetwork():    
    local_ip = ip_config.get_local_ip()
    local_network = ip_config.get_local_network(local_ip)
    print(f"Scanning network: {local_network}")

    results = await ip_config.scan_network_async(local_network)

    for ip, ports in results:
        if ports:
            print(f"{ip}:\t{ports}")

    return results


async def b_asyncgrab_banners(ips_with_ports):
    tasks = []
    ip_port_pairs = []

    for ip, ports in ips_with_ports:
        for port in ports:
            tasks.append(ip_config.async_grab_banner(ip, port))
            ip_port_pairs.append((ip, port))
    
    banners = await asyncio.gather(*tasks)
    return banners
def b_scan_publicnetwork():
    pass