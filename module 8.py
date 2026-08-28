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

def collecter_module_8_data():
    """Collecte les métriques brutes, les erreurs système et la télémétrie matérielle."""
    
    # 1. SERVICES SYSTEMD EN ÉCHEC
    failed_services = run_cmd("systemctl --failed --no-legend --no-pager 2>/dev/null | head -n 5")
    
    # 2. NOYAU TAINTED (Drapeaux d'altération du kernel)
    taint_val = run_cmd("cat /proc/sys/kernel/tainted 2>/dev/null")
    
    # 3. VULNÉRABILITÉS CPU DÉTAILLÉES
    cpu_vulns = run_cmd("tail -n +1 /sys/devices/system/cpu/vulnerabilities/* 2>/dev/null | head -n 12")
    
    # 4. SOCKETS RAW / AF_PACKET (Renifleurs de paquets)
    raw_sockets = run_cmd("ss -0 -a 2>/dev/null | head -n 5")
    
    # 5. AUTHENTIFICATION & PAM
    pam_files = run_cmd("ls -1 /etc/pam.d/ 2>/dev/null | head -n 8")
    
    # 6. UPTIME ET TEMPS D'INACTIVITÉ BRUTS (Secondes de fonctionnement / Secondes d'inactivité)
    uptime_raw = run_cmd("cat /proc/uptime 2>/dev/null")
    
    # 7. GENERATEUR DE HASARD MATÉRIEL (HW RNG)
    hw_rng = run_cmd("cat /sys/class/misc/hw_random/rng_current 2>/dev/null")

    return f"""
[16] AUDIT EXTRÊME & TÉLÉMÉTRIE BRUTE (MODULE 8)
------------------------------------------------------------------------

--- ⚠️ SERVICES SYSTEMD EN ÉCHEC ---
Services actuellement plantés ou en erreur :
{failed_services if failed_services and failed_services != "N/A" else "✅ Aucun service systemd en échec."}

--- ☣️ ALTÉRATION DU NOYAU (KERNEL TAINT) ---
Valeur Taint : {taint_val} (0 = Noyau 100% pur, >0 = Modules propriétaires ou erreurs matérielles)

--- 🛡️ FAILLES MICROARCHITECTURALES CPU (DÉTAILS) ---
{cpu_vulns if cpu_vulns and cpu_vulns != "N/A" else "Impossible de lire le dossier vulnerabilities."}

--- 👁️ CAPTURE DE PAQUETS BRUTS (AF_PACKET / RAW) ---
Sockets écoutant le réseau en mode brut :
{raw_sockets if raw_sockets and raw_sockets != "N/A" else "Aucun socket RAW suspect détecté."}

--- 🔐 MODULES D'AUTHENTIFICATION (PAM) ---
Fichiers de configuration PAM (/etc/pam.d/) :
{pam_files if pam_files and pam_files != "N/A" else "Accès refusé au dossier PAM."}

--- 📊 TÉLÉMÉTRIE SYSTEME & BRUIT MATÉRIEL ---
Uptime / Temps inactif brut (/proc/uptime) : {uptime_raw}
Source de hasard matériel (HW RNG)        : {hw_rng if hw_rng != "N/A" else "Aucune puce RNG matérielle active."}
========================================================================
"""

def injecter_module_8(nom_fichier="windows.txt"):
    """Injecte les métriques brutes et avancées dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' est introuvable. Exécute les modules précédents !")
        return
        
    print(f"[+] MODULE 8 ACTIVÉ : Injection de la télémétrie brute pour {nom_fichier}...")
    nouveau_contenu = collecter_module_8_data()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ SUCCÈS ! Le Module 8 a verrouillé la section [16] avec succès.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_8("windows.txt")
