# ==========================================
# MODULE 1 : BASE SCRIPT & INFOS SYSTÈMES
# ==========================================
import datetime
import getpass
import hashlib
import os
import platform
import shutil
import socket
import subprocess
import sys
import urllib.request

def run_cmd(cmd, timeout=2):
    """Exécute une commande shell en silence. Retourne 'N/A' en cas d'échec."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def obtenir_infos_etendues():
    """Collecte un maximum de données primaires pour initialiser le rapport."""
    hostname = socket.gethostname()
    utilisateur = getpass.getuser()
    
    # 1. IP Privée et Identifiants
    ips_privees = run_cmd("hostname -I")
    if ips_privees == "N/A" or not ips_privees:
        try:
            ips_privees = socket.gethostbyname(hostname)
        except Exception:
            ips_privees = "127.0.0.1"

    premiere_ip = ips_privees.split()[0] if ips_privees else "127.0.0.1"
    dernier_octet = premiere_ip.split(".")[-1] if "." in premiere_ip else "0"
    
    try:
        id_machine = f"PC-{int(dernier_octet):03d}"
    except ValueError:
        id_machine = "PC-000"
        
    hash_ip = hashlib.md5(premiere_ip.encode()).hexdigest()[:6].upper()

    # 2. IP Publique
    try:
        req = urllib.request.Request("https://api.ipify.org", headers={"User-Agent": "Mozilla/5.0"})
        ip_publique = urllib.request.urlopen(req, timeout=3).read().decode("utf-8")
    except Exception:
        ip_publique = "Non disponible"

    # 3. Réseau Avancé (Passerelle)
    passerelle = run_cmd("ip route show default | awk '/default/ {print $3}'")

    # 4. Temps d'activité (Uptime)
    uptime_str = "Inconnu"
    if os.path.exists("/proc/uptime"):
        try:
            with open("/proc/uptime") as f:
                uptime_seconds = float(f.readline().split()[0])
                heures = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                uptime_str = f"{heures}h {minutes}min"
        except Exception:
            pass

    # 5. OS & Environnement
    distro = "Linux"
    if os.path.exists("/etc/lsb-release"):
        with open("/etc/lsb-release") as f:
            for line in f:
                if line.startswith("DISTRIB_DESCRIPTION="):
                    distro = line.split("=")[1].strip().strip('"')
                    
    boot_mode = "UEFI" if os.path.exists("/sys/firmware/efi") else "BIOS Legacy"
    type_virt = run_cmd("systemd-detect-virt 2>/dev/null")
    env_virt = type_virt.capitalize() if type_virt and type_virt not in ["none", "N/A"] else "Bare-metal (Machine physique)"

    # 6. Matériel (CPU, RAM, Disque)
    cpu_nom = "Inconnu"
    if os.path.exists("/proc/cpuinfo"):
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        cpu_nom = line.split(":")[1].strip()
                        break
        except Exception:
            pass

    ram_total, ram_dispo = "Inconnue", "Inconnue"
    if os.path.exists("/proc/meminfo"):
        try:
            mem = {}
            with open("/proc/meminfo") as f:
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        mem[parts[0].strip()] = parts[1].strip()
            if "MemTotal" in mem:
                ram_total = f"{int(mem['MemTotal'].split()[0]) / (1024**2):.2f} Go"
            if "MemAvailable" in mem:
                ram_dispo = f"{int(mem['MemAvailable'].split()[0]) / (1024**2):.2f} Go"
        except Exception:
            pass

    total_disk, _, free_disk = shutil.disk_usage("/")
    disque_total = f"{total_disk / (1024**3):.1f} Go"
    disque_libre = f"{free_disk / (1024**3):.1f} Go"

    date_actuelle = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Construction du contenu formaté
    lignes = [
        "========================================================================",
        f"[1] RAPPORT DE DIAGNOSTIC INITIAL — {id_machine} ({hash_ip})",
        "========================================================================",
        f"Généré le            : {date_actuelle}",
        f"Session Utilisateur  : {utilisateur}",
        f"Nom de la machine    : {hostname}",
        f"Temps de marche      : {uptime_str}",
        "",
        "--- SYSTÈME D'EXPLOITATION ---",
        f"Distribution OS      : {distro}",
        f"Noyau (Kernel)       : {platform.release()}",
        f"Architecture         : {platform.machine()}",
        f"Version Python       : {sys.version.split()[0]}",
        f"Mode de démarrage    : {boot_mode}",
        f"Type d'environnement : {env_virt}",
        "",
        "--- MATÉRIEL & RESSOURCES ---",
        f"Processeur (CPU)     : {cpu_nom}",
        f"Mémoire RAM Totale   : {ram_total}",
        f"Mémoire RAM Dispo    : {ram_dispo}",
        f"Stockage Principal   : Total {disque_total} | Libre {disque_libre}",
        "",
        "--- RÉSEAU & CONNECTIVITÉ ---",
        f"IP(s) Privée(s)      : {ips_privees}",
        f"IP Publique          : {ip_publique}",
        f"Passerelle (Gateway) : {passerelle}",
        "========================================================================",
        ""
    ]
    return "\n".join(lignes)

def initialiser_rapport():
    nom_fichier = "windows.txt"
    contenu = obtenir_infos_etendues()

    try:
        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(contenu)
        print(f"[+] Succès : Le fichier '{nom_fichier}' a été créé/écrasé avec les données étendues du Module 1.")
        print("-" * 40)
        print(contenu)
    except Exception as e:
        print(f"[-] Erreur lors de la création du fichier : {e}")

if __name__ == "__main__":
    initialiser_rapport()
