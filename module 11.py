import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=5):
    """Exécute une commande shell de manière optimisée et retourne le résultat."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_peripheriques_fantomes():
    """Traque l'historique USB, les périphériques d'entrée et les bus mémoire."""
    
    # 1. TRACES USB : Nouveaux périphériques branchés (Historique du noyau)
    usb_new = run_cmd("dmesg 2>/dev/null | grep -i 'New USB device found' | tail -n 5 | awk -F']' '{print $2}'")
    
    # 2. TRACES USB : Périphériques débranchés/arrachés
    usb_disc = run_cmd("dmesg 2>/dev/null | grep -i 'USB disconnect' | tail -n 4 | awk -F']' '{print $2}'")
    
    # 3. POINTS D'ENTRÉE PHYSIQUES (Claviers, Souris, potentiels Keyloggers)
    # On regarde ce qui est branché dans /dev/input/by-id/
    inputs_hid = run_cmd("ls -l /dev/input/by-id/ 2>/dev/null | awk '{print $9 \" -> \" $11}' | grep -v '^->'")
    
    # 4. MODULES CACHÉS : Périphériques Humains (HID) chargés dans le noyau
    hid_modules = run_cmd("lsmod | grep -i hid | awk '{print $1 \" (\" $2/1024 \" Ko)\"}' | head -n 4")
    
    # 5. BUS MÉMOIRE BRUT (IOMEM - Adresses où le matériel écrit en direct)
    iomem_pci = run_cmd("cat /proc/iomem 2>/dev/null | grep -i 'PCI Bus' | head -n 5")
    
    # 6. OPTIMISATION MATÉRIELLE : PCIe Active State Power Management (ASPM)
    aspm_policy = run_cmd("cat /sys/module/pcie_aspm/parameters/policy 2>/dev/null")

    # Formatage de l'absence de logs (dmesg peut être restreint sans droits root)
    if not usb_new or usb_new == "N/A":
        usb_new = "⚠️ Impossible de lire l'historique (Droits Root requis pour dmesg ou logs vides)."
    if not usb_disc or usb_disc == "N/A":
        usb_disc = "Aucune déconnexion récente trouvée."

    return f"""
[19] PÉRIPHÉRIQUES FANTÔMES & BUS MATÉRIELS (MODULE 11)
------------------------------------------------------------------------

--- 🔌 HISTORIQUE USB (CONNEXIONS & DÉCONNEXIONS) ---
Derniers périphériques USB branchés sur la machine :
{usb_new}

Derniers périphériques USB débranchés (Traces de retrait) :
{usb_disc}

--- ⌨️ INTERFACES D'ENTRÉE (HID & KEYLOGGERS PHYSIQUES POTENTIELS) ---
Périphériques d'entrée actifs reconnus par le système (/dev/input) :
{inputs_hid if inputs_hid and inputs_hid != "N/A" else "Aucun périphérique d'entrée listé."}

Pilotes d'interfaces humaines (HID) chargés en mémoire :
{hid_modules if hid_modules and hid_modules != "N/A" else "Aucun module HID trouvé."}

--- ⚡ BUS MÉMOIRE & OPTIMISATION (PCIe) ---
Cartographie mémoire directe (IOMEM) - Plages du Bus PCI :
{iomem_pci if iomem_pci and iomem_pci != "N/A" else "Accès à /proc/iomem refusé."}

Politique d'énergie PCIe (ASPM) : {aspm_policy.strip() if aspm_policy != "N/A" else "Inconnue (ASPM désactivé)"}
========================================================================
"""

def injecter_module_11(nom_fichier="windows.txt"):
    """Injecte l'audit matériel et USB dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable. Ton projet ne peut pas être mis à jour !")
        return
        
    print(f"[+] MODULE 11 ACTIVÉ : Analyse optimisée des périphériques et bus matériels pour {nom_fichier}...")
    nouveau_contenu = collecter_peripheriques_fantomes()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ EXTRAORDINAIRE ! Le Module 11 a verrouillé la section [19].")
        print("Ton outil est maintenant capable de pister un appareil USB branché furtivement.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_11("windows.txt")
