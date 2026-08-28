import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=5):
    """Exécute une commande shell en silence."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_ultra_hardcore():
    """Récupère les paramètres de sécurité noyau et les mécanismes de persistance."""
    
    # 1. DÉFENSES NOYAU : ASLR (Address Space Layout Randomization)
    aslr_state = run_cmd("cat /proc/sys/kernel/randomize_va_space 2>/dev/null")
    if aslr_state == "2": aslr = "2 (Sécurité Maximale - Aléatoire total)"
    elif aslr_state == "1": aslr = "1 (Modérée - Aléatoire partiel)"
    else: aslr = f"{aslr_state} (⚠️ DÉSACTIVÉ ou Inconnu)"

    # 2. VULNÉRABILITÉ RÉSEAU : IP Forwarding (Routeur / Man-in-the-Middle)
    ip_fwd = run_cmd("cat /proc/sys/net/ipv4/ip_forward 2>/dev/null")
    ip_forwarding = "⚠️ ACTIVÉ (La machine peut router du trafic)" if ip_fwd == "1" else "✅ Désactivé"

    # 3. DÉBOGAGE KERNEL : Magic SysRq
    sysrq = run_cmd("cat /proc/sys/kernel/sysrq 2>/dev/null")
    
    # 4. PERSISTANCE FURTIVE : Services Systemd locaux (Espace utilisateur)
    systemd_user = run_cmd("ls -1 ~/.config/systemd/user/ 2>/dev/null | grep -E '\.service|\.timer'")
    
    # 5. TÂCHES PLANIFIÉES CACHÉES : Cron globaux (Niveau Système)
    cron_sys = run_cmd("ls -1 /etc/cron.d /etc/cron.daily 2>/dev/null | head -n 6")
    
    # 6. SURVEILLANCE MÉMOIRE : Segments de mémoire partagée (IPC)
    shared_mem = run_cmd("ipcs -m 2>/dev/null | awk 'NR>3 {print \"ID: \" $1 \" | Taille: \" $5/1024 \" Ko\"}' | head -n 4")
    
    # 7. INTRUSION EN DIRECT : Connexions SSH actuellement établies
    ssh_live = run_cmd("ss -tnp 2>/dev/null | grep ':22 ' | grep 'ESTAB'")

    return f"""
[14] PERSISTANCE & NOYAU PROFOND (MODULE 6)
------------------------------------------------------------------------

--- 🛡️ DÉFENSES DU NOYAU (KERNEL) ---
Protection Mémoire (ASLR) : {aslr}
Routage de paquets (IP Fwd): {ip_forwarding}
Touches Magiques (SysRq)   : {sysrq if sysrq != "N/A" else "Inconnu"} (0 = Désactivé, 1 = Total, >1 = Partiel)

--- 🕵️ PERSISTANCE & SERVICES FURTIFS ---
Services/Timers cachés dans le profil utilisateur (~/.config/systemd/user/) :
{systemd_user if systemd_user and systemd_user != "N/A" else "✅ Aucun service utilisateur suspect détecté."}

Tâches planifiées globales (Cron système - /etc/cron.d) :
{cron_sys if cron_sys and cron_sys != "N/A" else "Accès refusé ou dossiers vides."}

--- 🧠 MÉMOIRE BRUTE (IPC) ---
Segments de Mémoire Partagée actifs (Communication inter-processus) :
{shared_mem if shared_mem and shared_mem != "N/A" else "Aucune donnée IPC lisible."}

--- 🚨 ACTIVITÉ EN TEMPS RÉEL ---
Connexions SSH établies à la seconde précise :
{ssh_live if ssh_live and ssh_live != "N/A" else "✅ Aucune connexion SSH externe en cours."}
========================================================================
"""

def injecter_module_6(nom_fichier="windows.txt"):
    """Injecte la persistance et le noyau dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable.")
        return
        
    print(f"[+] MODULE 6 ACTIVÉ : Audit du Noyau et de la Persistance pour {nom_fichier}...")
    nouveau_contenu = collecter_ultra_hardcore()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ INCROYABLE ! Le Module 6 (Ultra Hardcore) a verrouillé la section [14].")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_6("windows.txt")
