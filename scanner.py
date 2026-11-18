import nmap

def scan_ports(target):
    try:
        # Direct path to Nmap executable
        scanner = nmap.PortScanner(
            nmap_search_path=(
                r"C:\Program Files (x86)\Nmap\nmap.exe",
            )
        )

        # Scan target
        scanner.scan(hosts=target, arguments="-sV")

        results = []

        for host in scanner.all_hosts():
            for protocol in scanner[host].all_protocols():
                for port in sorted(scanner[host][protocol].keys()):

                    port_info = scanner[host][protocol][port]

                    results.append({
                        "host": host,
                        "port": port,
                        "service": port_info.get("name", "Unknown"),
                        "product": port_info.get("product", ""),
                        "version": port_info.get("version", ""),
                        "status": port_info.get("state", "unknown")
                    })

        return results

    except Exception as e:
        return [{"error": str(e)}]