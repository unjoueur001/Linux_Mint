import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=8):
    """Exécute une commande optimisée via bash pour chaîner les opérations rapidement."""
    try:
        res = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_module_14_mega():
    """Traque Wi-Fi obscure, bases web massives et tentatives d'effacement de traces."""
    
    # --- PARTIE 1 : WI-FI OFFENSIF & TRACES DE CAPTURE ---
    # 1. Domaine de régulation (Contournement des lois de puissance d'antenne)
    reg_domain = run_cmd("iw reg get 2>/dev/null | grep -E 'country|DFS'")
    
    # 2. Traces de sniffer : Fichiers de capture Wi-Fi (Handshakes/PCAP) cachés
    pcap_files = run_cmd("find /tmp /var/tmp /home -maxdepth 3 -type f \\( -name '*.pcap' -o -name '*.cap' \\) 2>/dev/null | head -n 4")
    
    # --- PARTIE 2 : ABUS DES NAVIGATEURS ---
    # 3. Poids des bases de données locales (IndexedDB) : Sites stockant des données massives
    db_sizes = run_cmd("find ~/.config/google-chrome/ ~/.mozilla/ -type d -name 'IndexedDB' -exec du -sh {} + 2>/dev/null | sort -hr | head -n 3")
    
    # 4. Processus suspects accédant aux profils de navigation
    rogue_browsers = run_cmd("lsof +D ~/.config/google-chrome/ +D ~/.mozilla/ 2>/dev/null | awk 'NR>1 {print $1 \" (PID: \" $2 \")\"}' | sort | uniq | head -n 4")

    # --- PARTIE 3 : ANTI-FORENSICS (TRACES D'EFFACEMENT) ---
    # 5. Fichiers ZOMBIES : Supprimés du disque mais toujours maintenus en vie en RAM par un processus !
    deleted_in_ram = run_cmd("lsof +L1 2>/dev/null | grep -i 'deleted' | awk '{print \"Processus: \" $1 \" (PID: \" $2 \") maintient -> \" $9}' | head -n 5")
    
    # 6. Sabotage de l'historique Bash (Vérifie si les logs sont envoyés dans le vide)
    bash_size = run_cmd("ls -lah ~/.bash_history 2>/dev/null | awk '{print $5}'")
    bash_tamper = run_cmd("grep -iE 'HISTFILE=/dev/null|HISTSIZE=0' ~/.bashrc 2>/dev/null")
    
    # 7. Corbeilles profondes : Données jetées mais non purgées
    trash_size = run_cmd("du -sh ~/.local/share/Trash/ 2>/dev/null | awk '{print $1}'")

    return f"""
[22] DIAGNOSTIC WEB, SANS-FIL & ANTI-FORENSICS (MODULE 14)
------------------------------------------------------------------------

--- 📡 WI-FI : RÉGLEMENTATION & TRACES D'INTERCEPTION ---
Régulation d'antenne (Contournement de puissance potentiel) :
{reg_domain if reg_domain and reg_domain != "N/A" else "Impossible de lire le domaine de régulation."}

Traces de captures réseau (Fichiers .pcap / .cap potentiellement hostiles) :
{pcap_files if pcap_files and pcap_files != "N/A" else "✅ Aucun fichier de capture réseau suspect trouvé."}

--- 🌐 ABUS DES NAVIGATEURS & DONNÉES CACHÉES ---
Empreinte des bases de données locales (IndexedDB) :
{db_sizes if db_sizes and db_sizes != "N/A" else "Aucune base IndexedDB massive détectée."}

Processus accédant actuellement aux profils web :
{rogue_browsers if rogue_browsers and rogue_browsers != "N/A" else "Navigateurs éteints ou inaccessibles."}

--- 🕵️ ANTI-FORENSICS : TENTATIVES DE DISSIMULATION ---
Fichiers ZOMBIES (Supprimés physiquement mais encore cachés en RAM) :
{deleted_in_ram if deleted_in_ram and deleted_in_ram != "N/A" else "✅ Aucun fichier zombie détecté en mémoire."}

Intégrité de l'historique des commandes (Bash) :
Taille actuelle du log : {bash_size if bash_size and bash_size != "N/A" else "Fichier inexistant (Suspect)"}
Traces de sabotage   : {"⚠️ DÉTECTÉ (Historique désactivé)" if bash_tamper and bash_tamper != "N/A" else "✅ Historique actif."}

Poids des données dans la corbeille locale cachée : {trash_size if trash_size and trash_size != "N/A" else "0 Ko"}
========================================================================
"""

def injecter_module_14(nom_fichier="windows.txt"):
    """Injecte l'audit de niveau 14 (optimisé) dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable. Exécute d'abord les modules de base !")
        return
        
    print(f"[+] MODULE 14 ACTIVÉ : Lancement de l'audit Anti-Forensics et Wi-Fi avancé sur {nom_fichier}...")
    nouveau_contenu = collecter_module_14_mega()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ EXCEPTIONNEL ! Le Module 14 a verrouillé la section [22].")
        print("Ton fichier contient maintenant une analyse de fichiers zombies en RAM.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_14("windows.txt")
