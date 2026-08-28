import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=10):
    """Exécute une commande avec un délai plus long pour les recherches lourdes."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_hardcore_data():
    """Récupère les données très bas niveau et les failles potentielles."""
    
    # 1. SÉCURITÉ : Fichiers SUID (Top 5 dans les dossiers standards)
    suid = run_cmd("find /usr/bin /bin -perm -4000 -type f -exec ls -lh {} + 2>/dev/null | awk '{print $9}' | head -n 5")
    
    # 2. RÉSEAU FURTIF : Mode Promiscuous (Écoute totale)
    promisc = run_cmd("ip link | grep -i promisc")
    
    # 3. EXPOSITION : Ports ouverts sur 0.0.0.0 (Internet entier)
    exposed = run_cmd("ss -tulpn 2>/dev/null | grep '0.0.0.0:' | awk '{print $5 \" (\" $7 \")\"}' | head -n 5")
    
    # 4. SATURATION RÉSEAU : États des connexions TCP
    tcp_states = run_cmd("ss -ant 2>/dev/null | awk 'NR>1 {print $1}' | sort | uniq -c | sort -rn | head -n 5")
    
    # 5. DÉTOURNEMENT DNS : Lignes suspectes dans /etc/hosts
    hosts = run_cmd("grep -v '^#' /etc/hosts 2>/dev/null | grep -v '127.0.0.1' | grep -v '::1' | grep -v '^$'")
    
    # 6. LOGS CRITIQUES : Derniers échecs de mot de passe sudo
    sudo_fail = run_cmd("grep -i 'sudo.*authentication failure' /var/log/auth.log 2>/dev/null | tail -n 4")

    return f"""
[13] AUDIT HARDCORE & SÉCURITÉ OFFENSIVE (MODULE 5)
------------------------------------------------------------------------

--- 💀 VULNÉRABILITÉS & PRIVILÈGES (SUID) ---
Fichiers exécutables avec droits Root automatiques (Cibles d'attaques) :
{suid if suid and suid != "N/A" else "Aucun fichier SUID listé ou accès refusé."}

Derniers échecs d'authentification 'sudo' (Tentatives d'accès root) :
{sudo_fail if sudo_fail and sudo_fail != "N/A" else "Aucun échec sudo détecté (ou log inaccessible sans root)."}

--- 🕷️ RÉSEAU FURTIF & EXPOSITION ---
Interfaces réseau en mode Promiscuous (Écoute totale du trafic) :
{promisc if promisc and promisc != "N/A" else "Aucune interface en mode écoute furtive détectée."}

Services critiques directement exposés sur toutes les interfaces (0.0.0.0) :
{exposed if exposed and exposed != "N/A" else "Aucun port critique exposé globalement."}

États globaux des connexions TCP (Détection de saturation) :
{tcp_states if tcp_states and tcp_states != "N/A" else "Impossible de lire les états TCP."}

--- 🏴‍☠️ DÉTOURNEMENT DNS LOCAL ---
Redirections personnalisées dans /etc/hosts (Risque de détournement web) :
{hosts if hosts and hosts != "N/A" else "Fichier hosts propre (uniquement localhost système)."}
========================================================================
"""

def injecter_module_5(nom_fichier="windows.txt"):
    """Injecte les données hardcore dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable. Exécute les modules précédents !")
        return
        
    print(f"[+] MODULE 5 ACTIVÉ : Analyse de sécurité agressive pour {nom_fichier}...")
    nouveau_contenu = collecter_hardcore_data()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ MISSION ACCOMPLIE ! Le Module 5 a verrouillé la section [13]. Ton rapport est massif.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_5("windows.txt")
