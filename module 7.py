import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=5):
    """Exécute une commande shell et retourne le résultat nettoyé."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_module_7_data():
    """Collecte les données d'intégrité système, sysctl et stockage bas niveau."""
    
    # 1. INTÉGRITÉ DES BINAIRES CRITIQUES (Hashes SHA-256)
    hash_sudo = run_cmd("sha256sum /usr/bin/sudo 2>/dev/null | awk '{print $1}'")
    hash_bash = run_cmd("sha256sum /bin/bash 2>/dev/null | awk '{print $1}'")
    hash_login = run_cmd("sha256sum /bin/login 2>/dev/null | awk '{print $1}'")
    
    # 2. CAPACITÉS SPÉCIALES DES BINAIRES (Linux Capabilities)
    caps = run_cmd("getcap -r /usr/bin /usr/sbin /bin 2>/dev/null | head -n 6")
    
    # 3. PARAMÈTRES RÉSEAU DE DURCISSEMENT (SYSCTL)
    syncookies = run_cmd("sysctl net.ipv4.tcp_syncookies 2>/dev/null | awk '{print $3}'")
    rp_filter = run_cmd("sysctl net.ipv4.conf.all.rp_filter 2>/dev/null | awk '{print $3}'")
    icmp_echo = run_cmd("sysctl net.ipv4.icmp_echo_ignore_broadcasts 2>/dev/null | awk '{print $3}'")
    
    # 4. CHIFFREMENT & VOLUMES CRYPTÉS (LUKS / dm-crypt)
    crypto_vol = run_cmd("lsblk -o NAME,TYPE,FSTYPE,MOUNTPOINT 2>/dev/null | grep -i 'crypto_LUKS'")
    
    # 5. MÉTROLOGIE DISQUE & STATISTIQUES I/O (sysfs)
    disk_stats = run_cmd("cat /sys/block/sd*/stat 2>/dev/null | awk '{print \"Lectures: \" $1 \" | Écritures: \" $5}' | head -n 2")
    if not disk_stats or disk_stats == "N/A":
        disk_stats = run_cmd("cat /sys/block/nvme0n1/stat 2>/dev/null | awk '{print \"Lectures: \" $1 \" | Écritures: \" $5}'")

    return f"""
[15] INTÉGRITÉ, CAPACITÉS & MÉTROLOGIE AVANCÉE (MODULE 7)
------------------------------------------------------------------------

--- INTÉGRITÉ DES BINAIRES CRITIQUES (SHA-256) ---
/usr/bin/sudo : {hash_sudo}
/bin/bash     : {hash_bash}
/bin/login    : {hash_login}

--- CAPACITÉS LINUX SPÉCIALES (GETCAP) ---
Exécutables bénéficiant de privilèges granulaires sans être root :
{caps if caps and caps != "N/A" else "Aucune capacité spécifique détectée ou commande getcap absente."}

--- PARAMÈTRES SYSCTL DE PROTECTION RÉSEAU ---
Protection Syn Flood (tcp_syncookies) : {"Activé (1)" if syncookies == "1" else f"Désactivé ou valeur ({syncookies})"}
Anti-Spoofing (rp_filter)              : {"Activé (1 ou 2)" if rp_filter in ["1", "2"] else f"Désactivé ({rp_filter})"}
Ignore Broadcast ICMP                  : {"Activé (1)" if icmp_echo == "1" else f"Désactivé ({icmp_echo})"}

--- CHIFFREMENT & VOLUMES DISQUES ---
Partitions chiffrées (LUKS / dm-crypt) :
{crypto_vol if crypto_vol and crypto_vol != "N/A" else "Aucun volume LUKS actif détecté."}

--- STATISTIQUES D'ENTRÉE/SORTIE DISQUE (I/O) ---
E/S brutes du contrôleur principal :
{disk_stats if disk_stats and disk_stats != "N/A" else "Impossible de lire les métriques I/O."}
========================================================================
"""

def injecter_module_7(nom_fichier="windows.txt"):
    """Injecte les données d'intégrité et sysctl dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"Erreur : '{nom_fichier}' est introuvable. Exécute les modules précédents !")
        return
        
    print(f"[+] MODULE 7 ACTIVÉ : Collecte d'intégrité et de métrologie avancée pour {nom_fichier}...")
    nouveau_contenu = collecter_module_7_data()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("SUCCÈS ! Le Module 7 a ajouté la section [15] avec succès.")
    except Exception as e:
        print(f"Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_7("windows.txt")
