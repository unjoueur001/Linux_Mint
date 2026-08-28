import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=4):
    """Exécute une commande shell et retourne le résultat."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_tonne_de_donnees():
    """Récupère une quantité massive de métriques avancées et de sécurité."""
    
    # 1. MATÉRIEL PROFOND : BIOS & CPU Governor
    bios_version = run_cmd("cat /sys/class/dmi/id/bios_version 2>/dev/null")
    bios_date = run_cmd("cat /sys/class/dmi/id/bios_date 2>/dev/null")
    cpu_gov = run_cmd("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null")
    
    # 2. NOYAU & LIMITES (File Descriptors)
    # Renvoie 3 valeurs : nb alloués, nb libres, maximum autorisé par le noyau
    file_nr = run_cmd("cat /proc/sys/fs/file-nr 2>/dev/null")
    
    # 3. MODULES KERNEL (Top 5 des plus gros chargés en mémoire)
    modules_kernel = run_cmd("lsmod 2>/dev/null | awk 'NR>1 {print $1 \" (\" $2/1024 \" Ko)\"}' | head -n 5")

    # 4. SÉCURITÉ : Fichiers exécutables dans /tmp (Risque de sécurité)
    exec_tmp = run_cmd("find /tmp -type f -executable 2>/dev/null | head -n 5")
    nb_exec_tmp = run_cmd("find /tmp -type f -executable 2>/dev/null | wc -l")
    
    # 5. SÉCURITÉ : Clés SSH présentes
    cles_ssh = run_cmd("ls -1 ~/.ssh 2>/dev/null | grep -E 'id_rsa|id_ed25519|id_ecdsa|authorized_keys|known_hosts'")
    
    # 6. ACTIVITÉ & NETTOYAGE
    taille_corbeille = run_cmd("du -sh ~/.local/share/Trash 2>/dev/null | cut -f1")
    fichiers_modifies_24h = run_cmd("find ~ -type f -mtime -1 2>/dev/null | wc -l")
    
    # 7. RÉSEAU AVANCÉ : Table de routage brute
    routage = run_cmd("ip route 2>/dev/null")
    
    # 8. VARIABLES D'ENVIRONNEMENT CRITIQUES (Path & Shell)
    env_vars = run_cmd("env | grep -E '^(PATH|SHELL|USER)='")

    # Construction du gros bloc de texte
    return f"""
[11] AUDIT EXTRÊME & SYSTÈME PROFOND (MODULE 3)
------------------------------------------------------------------------

--- 🛠️ MATÉRIEL PROFOND ---
Version du BIOS / UEFI  : {bios_version if bios_version != "N/A" else "Inconnue"} (Date: {bios_date if bios_date != "N/A" else "Inconnue"})
Profil d'énergie CPU    : {cpu_gov.capitalize() if cpu_gov != "N/A" else "Non géré"}

--- 🧠 NOYAU & MÉMOIRE AVANCÉE ---
Fichiers ouverts (Noyau): {file_nr if file_nr != "N/A" else "Inconnu"} (Format: Actuels / Libres / Max)
Top 5 des modules Kernel les plus lourds chargés en RAM :
{modules_kernel if modules_kernel != "N/A" else "Impossible de lister lsmod"}

Variables d'environnement critiques :
{env_vars if env_vars != "N/A" else "Non détectées"}

--- 🔐 SÉCURITÉ & ANALYSE DE RISQUE ---
Fichiers d'identité SSH détectés dans le dossier local :
{cles_ssh if cles_ssh and cles_ssh != "N/A" else "Aucune clé SSH standard trouvée."}

Fichiers exécutables anormaux dans /tmp ({nb_exec_tmp.strip()} trouvés) :
{exec_tmp if exec_tmp and exec_tmp != "N/A" else "✅ Aucun exécutable suspect dans /tmp."}

--- 🗑️ NETTOYAGE & ACTIVITÉ RÉCENTE ---
Espace gaspillé par la Corbeille : {taille_corbeille if taille_corbeille and taille_corbeille != "N/A" else "0 Ko / Vide"}
Activité du profil : {fichiers_modifies_24h.strip() if fichiers_modifies_24h != "N/A" else "0"} fichier(s) modifié(s) par l'utilisateur ces dernières 24h.

--- 🌐 RÉSEAU AVANCÉ ---
Table de routage locale (IP Route) :
{routage if routage != "N/A" else "Impossible de lire la table de routage."}
========================================================================
"""

def injecter_module_3(nom_fichier="windows.txt"):
    """Injecte la tonne de données dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable. Lance les scripts précédents d'abord !")
        return
        
    print(f"[+] MODULE 3 ACTIVÉ : Collecte d'une tonne de données système pour {nom_fichier}...")
    nouveau_contenu = collecter_tonne_de_donnees()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ BOOM ! Le Module 3 a injecté avec succès la section [11] Tout à la fin du fichier.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_3("windows.txt")
