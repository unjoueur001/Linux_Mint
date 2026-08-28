import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=5):
    """Exécute une commande shell et retourne le résultat."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_forensic_et_caches():
    """Récupère les traces utilisateurs, threads et infos bas niveau."""
    
    # 1. TRACES : Les 5 dernières commandes tapées dans le terminal bash/zsh
    historique = run_cmd("tail -n 5 ~/.bash_history 2>/dev/null || tail -n 5 ~/.zsh_history 2>/dev/null")
    
    # 2. UTILISATEURS : Ceux qui ont un vrai shell de connexion (pas les comptes services)
    vrais_users = run_cmd("grep -E '(/bash|/zsh)$' /etc/passwd | awk -F':' '{print $1 \" (Shell: \" $7 \")\"}'")
    
    # 3. THREADS & PROCESSUS : Nombre de threads totaux et le doyen des processus
    nb_threads = run_cmd("ps -eT 2>/dev/null | wc -l")
    vieux_process = run_cmd("ps -eo pid,lstart,cmd --sort=start_time 2>/dev/null | head -n 2 | tail -n 1")

    # 4. CPU CACHES : Tailles des caches L1, L2, L3
    caches_cpu = run_cmd("lscpu 2>/dev/null | grep -i 'cache' | sed 's/  */ /g'")
    
    # 5. DISQUE & CACHES CACHÉS : Dossiers invisibles les plus lourds
    user_home = os.path.expanduser("~")
    gros_dossiers_caches = run_cmd(f"du -sh {user_home}/.[!.]* 2>/dev/null | sort -rh | head -n 5")
    
    # 6. POINTS DE MONTAGE : Les disques les plus remplis (hors loop/snap)
    disques_pleins = run_cmd("df -h 2>/dev/null | grep -v 'loop' | grep -v 'tmpfs' | sort -hk 5 -r | head -n 4")
    
    # 7. RÉSEAU PHYSIQUE : Table ARP (Adresses MAC associées aux IP locales)
    arp_table = run_cmd("ip neigh show 2>/dev/null")

    # On compile cette tonne de données
    return f"""
[12] FORENSIC, CACHES & TRACES (MODULE 4)
------------------------------------------------------------------------

--- 🕵️ TRACES & UTILISATEURS ---
Utilisateurs système avec un accès Terminal complet :
{vrais_users if vrais_users != "N/A" else "Impossible de lire /etc/passwd"}

Les 5 dernières commandes tapées dans ton historique terminal :
{historique if historique and historique != "N/A" else "Aucun historique trouvé (ou vidé)."}

--- 🖥️ PROCESSEURS & THREADS ---
Nombre total de Threads actifs : {nb_threads.strip() if nb_threads != "N/A" else "Inconnu"}
Le plus vieux processus en cours d'exécution (PID | Date de lancement | Commande) :
{vieux_process if vieux_process != "N/A" else "Impossible de lister les processus"}

Tailles des Caches CPU (L1, L2, L3) :
{caches_cpu if caches_cpu != "N/A" else "Commande lscpu non disponible"}

--- 📂 ESPACE DISQUE & DOSSIERS CACHÉS ---
Top 5 des plus gros dossiers CACHÉS (souvent des caches d'applications) dans {user_home} :
{gros_dossiers_caches if gros_dossiers_caches and gros_dossiers_caches != "N/A" else "Impossible de scanner les fichiers cachés."}

Les partitions physiques les plus proches de la saturation :
{disques_pleins if disques_pleins != "N/A" else "Impossible de lire l'espace disque."}

--- 📡 RÉSEAU PHYSIQUE (ARP) ---
Table ARP (Machines qui discutent physiquement avec ta carte réseau) :
{arp_table if arp_table and arp_table != "N/A" else "Table ARP vide ou inaccessible."}
========================================================================
"""

def injecter_module_4(nom_fichier="windows.txt"):
    """Injecte les données forensic dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable. Ton projet ne peut pas être mis à jour sans le fichier de base !")
        return
        
    print(f"[+] MODULE 4 ACTIVÉ : Analyse forensic et hardware profond pour {nom_fichier}...")
    nouveau_contenu = collecter_forensic_et_caches()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ INCROYABLE ! Le Module 4 a ajouté la section [12] tout à la fin du fichier.")
        print("Ton fichier d'audit est maintenant une véritable encyclopédie sur ton système !")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_4("windows.txt")
