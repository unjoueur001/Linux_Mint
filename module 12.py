import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=8):
    """Exécute une commande shell de manière optimisée avec un timeout un peu plus long pour le scan Wi-Fi."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_darknet_et_apps():
    """Traque le Wi-Fi, les ports UDP, le pare-feu et l'inventaire logiciel."""
    
    # 1. INVENTAIRE APPLICATIF : Nombre total de logiciels/paquets installés (Basé sur Debian/Ubuntu)
    total_apps = run_cmd("dpkg-query -f '${binary:Package}\n' -W 2>/dev/null | wc -l")
    
    # 2. INVENTAIRE APPLICATIF : Le Top 10 des logiciels les plus lourds (en Ko)
    top_lourds = run_cmd("dpkg-query -W -f='${Installed-Size} Ko\t-> ${Package}\n' 2>/dev/null | sort -n -r | head -n 10")
    if not top_lourds or top_lourds == "N/A":
        # Alternative si le système est RedHat/Fedora au lieu de Debian/Ubuntu
        top_lourds = run_cmd("rpm -qa --queryformat '%{SIZE}\t-> %{NAME}\n' 2>/dev/null | sort -n -r | head -n 10")
    
    # 3. TERRAIN WI-FI : Interfaces sans-fil disponibles
    wifi_interfaces = run_cmd("iw dev 2>/dev/null | grep -E 'Interface|type|addr' | awk '{$1=$1;print}'")
    
    # 4. TERRAIN WI-FI : Scan des réseaux environnants (Nécessite souvent NetworkManager)
    wifi_scan = run_cmd("nmcli -t -f SSID,BSSID,SIGNAL,SECURITY dev wifi 2>/dev/null | head -n 8 | sed 's/:/ | /g'")
    
    # 5. DARK NETWORK : Ports UDP ouverts (Souvent utilisés pour le P2P, VPN ou malwares furtifs)
    udp_ports = run_cmd("ss -ulnp 2>/dev/null | awk 'NR>1 {print $5 \" (Processus: \" $6 \")\"}' | head -n 6")
    
    # 6. FILTRAGE NOYAU : Règles de Pare-feu actives (iptables)
    firewall_rules = run_cmd("iptables-save 2>/dev/null | grep -E '^-A' | head -n 8")
    
    # 7. BLINDAGE APPLICATIF : AppArmor ou SELinux (Confinement des processus)
    apparmor = run_cmd("aa-status --head 2>/dev/null | head -n 2")
    selinux = run_cmd("sestatus 2>/dev/null | grep 'SELinux status' | awk '{print $3}'")
    
    blindage = ""
    if apparmor and apparmor != "N/A": blindage += f"AppArmor : {apparmor}\n"
    if selinux and selinux != "N/A": blindage += f"SELinux : {selinux}\n"
    if not blindage: blindage = "Aucun blindage restrictif détecté (ou droits Root requis)."

    return f"""
[20] DARK NETWORK, WI-FI & INVENTAIRE APPLICATIF (MODULE 12)
------------------------------------------------------------------------

--- 📦 INVENTAIRE LOGICIEL & VOLUMÉTRIE ---
Nombre total de paquets/applications installés : {total_apps.strip() if total_apps != "N/A" else "Inconnu"}
Top 10 des programmes qui consomment le plus d'espace sur le disque :
{top_lourds if top_lourds and top_lourds != "N/A" else "Impossible de lire la base de données des paquets."}

--- 📡 RADIOGRAPHIE WI-FI & ONDES ---
Interfaces Wi-Fi physiques détectées :
{wifi_interfaces if wifi_interfaces and wifi_interfaces != "N/A" else "Aucune carte Wi-Fi reconnue."}

Scan de l'environnement (SSID | BSSID | Signal | Chiffrement) :
{wifi_scan if wifi_scan and wifi_scan != "N/A" else "Scan Wi-Fi indisponible (NetworkManager absent ou droits requis)."}

--- 🕸️ DARK NETWORK & UDP FANTÔMES ---
Sockets UDP en écoute silencieuse (Protocoles sans connexion) :
{udp_ports if udp_ports and udp_ports != "N/A" else "Aucun port UDP critique en écoute."}

--- 🧱 PARE-FEU NOYAU & BLINDAGE ---
Règles de filtrage directes (iptables - Premières règles actives) :
{firewall_rules if firewall_rules and firewall_rules != "N/A" else "Aucune règle iptables visible ou droits Root manquants."}

État des boucliers de confinement (AppArmor / SELinux) :
{blindage}
========================================================================
"""

def injecter_module_12(nom_fichier="windows.txt"):
    """Injecte l'audit Wi-Fi, Applicatif et Réseau dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable. Ton script principal doit être exécuté avant !")
        return
        
    print(f"[+] MODULE 12 ACTIVÉ : Scan du Terrain Wi-Fi et Inventaire Massif pour {nom_fichier}...")
    nouveau_contenu = collecter_darknet_et_apps()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ GIGANTESQUE ! Le Module 12 a verrouillé la section [20].")
        print("Ton rapport contient maintenant l'environnement physique (Wi-Fi) et l'inventaire des programmes.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_12("windows.txt")
