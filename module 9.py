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

def collecter_les_abysses():
    """Récupère les données obscures du noyau, de la carte mère et de la RAM."""
    
    # 1. FIRMWARE CACHÉ : Variables EFI de la carte mère
    nb_efi = run_cmd("ls -1 /sys/firmware/efi/efivars/ 2>/dev/null | wc -l")
    efi_samples = run_cmd("ls -1 /sys/firmware/efi/efivars/ 2>/dev/null | head -n 3")
    if not nb_efi or nb_efi == "N/A": nb_efi = "0 (Système en mode BIOS Legacy ou accès bloqué)"
    
    # 2. COFFRE-FORT KERNEL : Le Keyring
    keys_count = run_cmd("cat /proc/keys 2>/dev/null | wc -l")
    keys_meta = run_cmd("cat /proc/keys 2>/dev/null | awk '{print $1 \" \" $8 \" \" $9}' | head -n 4")
    
    # 3. TABLES ACPI (Matériel brut)
    acpi_tables = run_cmd("ls -sh /sys/firmware/acpi/tables/ 2>/dev/null | head -n 4")
    
    # 4. SÉCURITÉ PROFONDE : kptr_restrict (Cacher l'emplacement du noyau en RAM)
    kptr = run_cmd("cat /proc/sys/kernel/kptr_restrict 2>/dev/null")
    if kptr == "2": kptr_status = "2 (Maximal - Adresses noyaux totalement invisibles)"
    elif kptr == "1": kptr_status = "1 (Partiel - Caché aux utilisateurs normaux)"
    else: kptr_status = f"{kptr} (⚠️ Vulnérable - Adresses exposées)"

    # 5. OOM KILLER : Le processus le plus proche de se faire "tuer" par le système
    oom_max = run_cmd("cat /proc/*/oom_score 2>/dev/null | sort -n | tail -n 1")
    
    # 6. ISOLATION MATÉRIELLE (IOMMU)
    iommu_groups = run_cmd("ls -1 /sys/kernel/iommu_groups/ 2>/dev/null | wc -l")
    if iommu_groups == "0" or iommu_groups == "N/A":
        iommu_status = "Désactivé ou non supporté par le CPU/Carte mère"
    else:
        iommu_status = f"ACTIVÉ ({iommu_groups.strip()} groupes d'isolation détectés)"

    return f"""
[17] ARTEFACTS CACHÉS & FIRMWARE PROFOND (MODULE 9)
------------------------------------------------------------------------

--- 🧬 MÉMOIRE FIRMWARE (NVRAM / EFI) ---
Nombre de variables EFI injectées par la carte mère : {nb_efi}
Exemples d'artefacts EFI :
{efi_samples if efi_samples and efi_samples != "N/A" else "Aucune variable lisible."}

Tables matérielles ACPI brutes :
{acpi_tables if acpi_tables and acpi_tables != "N/A" else "Accès ACPI refusé."}

--- 🗝️ COFFRE-FORT DU NOYAU (KERNEL KEYRING) ---
Entrées dans le trousseau de clés secret du noyau : {keys_count.strip() if keys_count != "N/A" else "Inconnu"}
Métadonnées des premières clés (ID / Type / Description) :
{keys_meta if keys_meta and keys_meta != "N/A" else "Trousseau inaccessible."}

--- 🛡️ SÉCURITÉ & ARCHITECTURE INVISIBLE ---
Restriction des pointeurs noyaux (kptr_restrict) : {kptr_status}
Isolation de la mémoire matérielle (IOMMU)      : {iommu_status}

--- 💀 JUGEMENT DU NOYAU (OOM KILLER) ---
Score OOM le plus élevé actuellement attribué à un processus : {oom_max if oom_max != "N/A" else "Inconnu"} 
(Si la RAM sature, ce processus sera exécuté de force par le noyau).
========================================================================
"""

def injecter_module_9(nom_fichier="windows.txt"):
    """Injecte les données abyssales dans le rapport de project V?."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable.")
        return
        
    print(f"[+] MODULE 9 ACTIVÉ : Exploration des artefacts invisibles pour {nom_fichier}...")
    nouveau_contenu = collecter_les_abysses()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ INCROYABLE ! Le Module 9 a verrouillé la section [17].")
        print("Ton outil scrute maintenant des zones que 99% des utilisateurs ignorent.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_9("windows.txt")
