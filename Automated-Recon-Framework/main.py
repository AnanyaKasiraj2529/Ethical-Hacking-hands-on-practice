import json
from modules.dns_enum import dns_lookup
from modules.port_scan import scan_ports
from modules.nmap_scan import run_nmap
from modules.http_analysis import analyze_http
from modules.vuln_analysis import extract_cves, calculate_risk_score


def main():
    target = input("Enter target domain or IP: ")

    print("[+] Running DNS enumeration...")
    dns_results = dns_lookup(target)

    print("[+] Running Python port scan...")
    ports = scan_ports(target)

    print("[+] Running advanced Nmap scan...")
    nmap_results = run_nmap(target)

    print("[+] Extracting CVEs...")
    cves = extract_cves(nmap_results)

    print("[+] Running HTTP analysis...")
    headers = analyze_http(target)

    risk = calculate_risk_score(ports, cves)

    report = {
        "target": target,
        "dns": dns_results,
        "open_ports_python": ports,
        "cves_detected": cves,
        "risk_level": risk,
        "nmap_details": nmap_results,
        "http_headers": headers
    }

    with open("output/recon_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\n========== Recon Summary ==========")
    print(f"Target: {target}")
    print(f"Open Ports: {ports}")
    print(f"CVEs Found: {cves}")
    print(f"Calculated Risk Level: {risk}")
    print("===================================")
    print("[+] Full report saved in output/recon_report.json")


if __name__ == "__main__":
    main()
