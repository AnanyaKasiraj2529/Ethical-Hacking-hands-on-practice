---

# 🧪 Testing Against Metasploitable 2 (Controlled Lab Validation)

## Lab Environment Setup

| Component | Platform |
|------------|------------|
| Attacker | Kali Linux (VirtualBox) |
| Target | Metasploitable 2 (VMware) |
| Network Mode | NAT |
| Scan Tool | Nmap |
| Framework | Python Recon Engine |

---

## Step 1 — Start Metasploitable 2

Login credentials:
Username: msfadmin
Password: msfadmin


Check target IP:

```bash
ifconfig
```
Example:
```bash
inet addr:192.168.xx.xxx
Step 2 — Verify Connectivity from Kali
ping 192.168.xx.xxx
```
Successful replies confirm network communication.

Step 3 — Manual Nmap Validation

Before running the framework, manual validation was performed:
```bash
nmap -T4 -F -sV 192.168.xx.xxx
```
Observed open services:
FTP (21)
SSH (22)
Telnet (23)
SMTP (25)
HTTP (80)
MySQL (3306)

Step 4 — Run Automated Recon Framework
```bash
source venv/bin/activate
python main.py
```
Enter:

192.168.xx.xxx
Sample Automated Output
```bash
========== Recon Summary ==========
Target: 192.168.56.101
Open Ports: [21, 22, 23, 25, 80, 3306]
Calculated Risk Level: HIGH
===================================
```
Risk Analysis Observations
Metasploitable 2 exposes:
- Plaintext authentication services (FTP, Telnet)
- Database services (MySQL)
- Outdated web server versions
- Multiple remote attack surfaces
- The framework correctly classifies this exposure as HIGH risk.
 Ethical Notice:
**All testing was conducted in a controlled lab environment using intentionally vulnerable systems. No unauthorized scanning was performed on external networks.
---

