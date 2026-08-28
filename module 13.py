import os
import subprocess
from pathlib import Path

def run_cmd(cmd, timeout=5):
    """Exécute une commande shell de manière furtive et retourne le résultat."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return res.stdout.strip() if res.returncode == 0 else "N/A"
    except Exception:
        return "N/A"

def collecter_wifi_sombre():
    """Traque les capacités d'attaque, les secrets et les voisins Wi-Fi."""
    
    # 1. CAPACITÉS OFFENSIVES : Support du mode "Monitor" (Écoute globale)
    monitor_mode = run_cmd("iw list 2>/dev/null | grep -A 8 'Supported interface modes' | grep 'monitor'")
    
    # 2. PUISSANCE BRUTE : Puissance de transmission de l'antenne (Tx-Power)
    tx_power = run_cmd("iwconfig 2>/dev/null | grep -i 'Tx-Power' | awk '{print $1 \" \" $4 \" \" $5}'")
    
    # 3. SECRETS EN CLAIR : Extraction des mots de passe Wi-Fi (Nécessite droits Root)
    psk_keys = run_cmd("grep -h '^psk=' /etc/NetworkManager/system-connections/* 2>/dev/null | head -n 5")
    if not psk_keys or psk_keys == "N/A":
        psk_keys = "🔒 Accès refusé (Root requis) ou aucun mot de passe stocké en clair."
        
    # 4. CARTOGRAPHIE LOCALE : Appareils cachés sur le même réseau (Table ARP/Voisins)
    voisins_arp = run_cmd("ip neigh show 2>/dev/null | grep -v 'FAILED' | awk '{print \"IP: \" $1 \" | MAC: \" $5 \" | État: \" $6}' | head -n 6")
    
    # 5. DÉTECTION D'ATTAQUE : Traces de "Deauthentication" (Expulsions forcées)
    deauth_logs = run_cmd("dmesg 2>/dev/null | grep -i 'deauthenticated' | tail -n 4 | awk -F']' '{print $2}'")

    return f"""
[21] WI-FI SOMBRE & ESPIONNAGE LOCAL (MODULE 13)
------------------------------------------------------------------------

--- 📡 CAPACITÉS OFFENSIVES MATÉRIELLES ---
Support du Mode Monitor (Injection & Capture globale) :
{"✅ DÉTECTÉ - Carte compatible Pentest Wi-Fi" if monitor_mode and monitor_mode != "N/A" else "❌ Non supporté (ou iw list indisponible)"}

Puissance d'émission (Tx-Power) :
{tx_power if tx_power and tx_power != "N/A" else "Impossible de lire la puissance d'antenne."}

--- 🔑 RÉCOLTE DE SECRETS WI-FI (CREDENTIALS) ---
Mots de passe bruts extraits du système (Pre-Shared Keys) :
{psk_keys}

--- 👁️ ESPIONNAGE DES VOISINS (TABLE ARP) ---
Appareils actuellement connectés autour de toi sur le même réseau :
{voisins_arp if voisins_arp and voisins_arp != "N/A" else "Aucun voisin détecté dans le cache ARP."}

--- 🚨 DÉTECTION D'ATTAQUES (DEAUTH / JAMMING) ---
Traces récentes d'attaques de déconnexion forcée (Logs Noyau) :
{deauth_logs if deauth_logs and deauth_logs != "N/A" else "✅ Aucun log de déconnexion hostile détecté."}
========================================================================
"""

def injecter_module_13(nom_fichier="windows.txt"):
    """Injecte l'audit Wi-Fi obscur dans le rapport."""
    fichier = Path(nom_fichier)
    
    if not fichier.exists():
        print(f"❌ Erreur : '{nom_fichier}' introuvable. Exécute la base avant !")
        return
        
    print(f"[+] MODULE 13 ACTIVÉ : Analyse Wi-Fi Sombre et Espionnage pour {nom_fichier}...")
    nouveau_contenu = collecter_wifi_sombre()
    
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print("✅ TERRIFIANT ! Le Module 13 a verrouillé la section [21].")
        print("Ton outil scrute maintenant les mots de passe en clair et les attaques environnantes.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'écriture : {e}")

if __name__ == "__main__":
    injecter_module_13("windows.txt")
