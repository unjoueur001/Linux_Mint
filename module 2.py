import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=3):
    """Exécute une commande shell et retourne le résultat nettoyé."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_nouvelles_choses():
    """Récupère des données inédites pour enrichir le rapport."""
    
    # 1. Mémoire disponible réelle
    mem_avail = run_cmd("grep MemAvailable /proc/meminfo | awk '{print $2/1024 \" Mo\"}'")
    
    # 2. Historique des derniers redémarrages
    reboots = run_cmd("last reboot | head -n 4")
    
    # 3. Top 5 des plus gros dossiers dans le dossier de l'utilisateur
    user_home = os.path.expanduser("~")
    gros_dossiers = run_cmd(f"du -sh {user_home}/* 2>/dev/null | sort -rh | head -n 5")
    
    # 4. Températures détaillées
    temps = run_cmd("sensors 2>/dev/null | grep -E 'Core|Package|temp' | head -n 5")
    if not temps or temps == "N/A":
        temps = "(L'outil lm-sensors n'est pas installé ou n'a pas accès aux sondes)"
        
    # 5. Utilisateurs actuellement connectés
    users_log = run_cmd("who")

    # 6. Entropie du système
    entropie = run_cmd("cat /proc/sys/kernel/random/entropy_avail")
    
    # On prépare le texte qui sera ajouté à la fin du fichier
    return f"""
[10] ENRICHISSEMENT : MÉTRIQUES SUPPLÉMENTAIRES
------------------------------------------------------------------------
Mémoire Disponible (Réelle) : {mem_avail if mem_avail != "N/A" else "Inconnue"}
Entropie du système (Crypto): {entropie} bits (Idéalement > 2000)

Utilisateurs actuellement connectés au système :
{users_log if users_log and users_log != "N/A" else "Seul ton utilisateur semble connecté."}

Historique des derniers redémarrages :
{reboots if reboots and reboots != "N/A" else "Aucune information de redémarrage trouvée."}

Top 5 des dossiers les plus lourds dans {user_home} :
{gros_dossiers if gros_dossiers and gros_dossiers != "N/A" else "Impossible d'analyser l'espace disque du dossier utilisateur."}

Relevé des capteurs thermiques (CPU / Carte mère) :
{temps}
"""

def modifier_fichier(nom_fichier="windows.txt"):
    """Ouvre le fichier existant et ajoute les nouvelles données à la fin."""
    fichier = Path(nom_fichier)
    
    # On vérifie si le fichier windows.txt existe bien
    if not fichier.exists():
        print(f"❌ Erreur : Le fichier '{nom_fichier}' est introuvable.")
        print("💡 Astuce : Lance d'abord ton premier script pour le créer !")
        return
        
    print(f"[+] Analyse en cours... Collecte de PLUS de données pour {nom_fichier} !")
    texte_en_plus = collecter_nouvelles_choses()
    
    try:
        # L'ouverture en mode "a" (append) permet d'ajouter à la fin sans effacer le reste
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(texte_en_plus)
        print(f"✅ SUCCÈS ! Le fichier '{nom_fichier}' a été enrichi avec succès.")
        print("Ouvre-le pour voir la nouvelle section [10] tout en bas !")
    except Exception as e:
        print(f"❌ Erreur lors de la modification du fichier : {e}")

if __name__ == "__main__":
    modifier_fichier("windows.txt")
