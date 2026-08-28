import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=5):
    """Exécute une commande shell en silence et retourne le résultat."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_fantomes_ram():
    """Traque les systèmes éphémères et l'activité invisible en mémoire."""
    
    # 1. SYSTÈMES VIRTUELS EN RAM (tmpfs)
    tmpfs_usage = run_cmd("df -h -t tmpfs -t devtmpfs 2>/dev/null | awk 'NR>1 {print $6 \" (\" $2 \" alloués, \" $4 \" libres)\"}'")
    
    # 2. TUNNELS INVISIBLES : Named Pipes (FIFOs) dans les répertoires temporaires
    pipes = run_cmd("find /tmp /run /var/run -type p 2>/dev/null | head -n 5")
    
    # 3. GESTION DE MÉMOIRE MASSIVE (Transparent HugePages)
    thp_state = run_cmd("cat /sys/kernel/mm/transparent_hugepage/enabled 2>/dev/null")
    if thp_state == "N/A": thp_state = "Non supporté par ce noyau."
    
    # 4. PRISONS DU NOYAU (Seccomp)
    # Compte le nombre de processus activement isolés par Seccomp
    seccomp_count = run_cmd("grep -s -l 'Seccomp:[[:space:]]*[12]' /proc/[0-9]*/status 2>/dev/null | wc -l")
    
    # 5. TRACES DE CODE NOYAU DYNAMIQUE (eBPF)
    ebpf_maps = run_cmd("ls -1 /sys/fs/bpf 2>/dev/null | wc -l")
    if ebpf_maps == "0" or ebpf_maps == "N/A":
        ebpf_status = "0 (Aucun objet eBPF détecté dans le système de fichiers)"
    else:
        ebpf_status = f"{ebpf_maps.strip()} objets eBPF actifs (Surveillance système ou Rootkit potentiel)"

    # 6. CACHE SLAB DU NOYAU (Mémoire de travail du kernel)
    slab_top = run_cmd("cat /proc/slabinfo 2>/dev/null | awk 'NR>2 {print $1}' | head -n 4")
    if not slab_top or slab_top == "N/A":
        slab_top = "⚠️ Accès refusé (/proc/slabinfo nécessite souvent les droits root)"

    return f"""
[18] FANTÔMES EN RAM & MÉCANISMES ÉPHÉMÈRES (MODULE 10)
------------------------------------------------------------------------

--- ☁️ SYSTÈMES DE FICHIERS VIRTUELS (RAM PURE) ---
Points de montage évaporables (tmpfs / devtmpfs) :
{tmpfs_usage if tmpfs_usage and tmpfs_usage != "N/A" else "Aucun système tmpfs standard monté."}

Tunnels de communication invisibles (Named Pipes / FIFOs dans /tmp et /run) :
{pipes if pipes and pipes != "N/A" else "Aucun tunnel FIFO détecté."}

--- 🧩 ARCHITECTURE MÉMOIRE AVANCÉE ---
Transparent HugePages (THP) : {thp_state}
Objets principaux dans le cache SLAB (Travail interne du noyau) :
{slab_top}

--- 🛡️ ISOLATION & CODE DYNAMIQUE ---
Processus sous isolation stricte (Seccomp Sandboxing) : {seccomp_count.strip() if seccomp_count != "N/A" else "0"} processus emprisonnés.
Traces d'injections eBPF actives (Berkeley Packet Filter) : {ebpf_status}
========================================================================
"""

def injecter_module_10(nom_fichier="windows.txt"):
    """Injecte les fantômes RAM dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable. Ton projet ne peut pas être mis à jour !")
        return
        
    print(f"[+] MODULE 10 ACTIVÉ : Chasse aux fantômes en RAM pour {nom_fichier}...")
    nouveau_contenu = collecter_fantomes_ram()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ INCROYABLE ! Le Module 10 a verrouillé la section [18].")
        print("Ton outil surveille maintenant des mécanismes dont la plupart des admins système ignorent l'existence.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_10("windows.txt")
