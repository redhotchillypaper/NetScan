# NetScan

Lightweight Python tool for scanning devices on a local network.

## What it does

- Finds devices using ARP table
- Scans common ports
- Prints clean results

## Usage

```bash
python main.py 
```
## Example
OPEN IPS/PORTS:
x.x.2.1:53 -> open
x.x.2.43:62078 -> open

DEVICES in the local network (3):
---------------
HomeWiFi.net
IP:x.x.2.1
MAC:x:x:x:x:x:x
Available ports:[53]
---------------
MacBook-Air
IP:x.x.2.14
MAC:x:x:x:x:x:x
Available ports:[]
---------------
googlewebostv
IP:x.x.2.43
MAC:x:x:x:x:x:x
Available ports:[62078]