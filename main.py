import ipaddress
import socket
import ip_manipulations as ipm




def grab_banner(ip, port, timeout=2):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))

        s.send(b"GET / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024)
        s.close()
        return banner.decode(errors="ignore")
    except Exception as e:
        return f"Error: {e}"

def main():

    local_ip = ipm.get_local_ip()
    network = ipm.get_local_network(local_ip)
    port_to_check = 80
    alive = ipm.scan_network(network, port_to_check)
    print(f"Live connections with open port {port_to_check}: {alive}")
    # response = grab_banner("192.168.68.1", 80) 
    # print("\nResponse:\n" + response)


if __name__ == "__main__":
    main()










# import subprocess
# import platform

# def ping(host):
#     param = '-n' if platform.system().lower()=='windows' else '-c'
#     command = ['ping', param, '1', host]
#     return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

# network = "192.168.1.0/24"
# import ipaddress

# alive_hosts = []
# for ip in ipaddress.ip_network(network).hosts():
#     ip_str = str(ip)
#     if ping(ip_str):
#         print(f"[+] {ip_str} живий (ping ok)")
#         alive_hosts.append(ip_str)
#     else:
#         print(f"[-] {ip_str} не відповідає")
# print(f"Живі хости: {alive_hosts}")
