import requests
import json

json_file = "urls.json"
output_file = "lists/blocked_domains.txt"
max_size = 100 * 1024 * 1024  # 100 MB


def load_urls_from_json(json_file):
    # Lädt die URLs aus der JSON-Datei.
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
            return data.get("urls", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Fehler beim Laden der JSON-Datei: {e}")
        return []


def fetch_list(url):
    # Lädt die Inhalte der URL herunter und Löscht unnötige Kommentare
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Liste von {url}: {e}")
        return []


def remove_duplicates(domains):
    return list(set(domains))


def download():
    # URLs aus der JSON-Datei laden
    list_urls = load_urls_from_json(json_file)
    if not list_urls:
        print("Keine gültigen URLs in der JSON-Datei gefunden.")
        return

    all_domains = []

    # Inhalte der Listen abrufen und kombinieren
    for index, url in enumerate(list_urls, 1):
        print(f"[{index}/{len(list_urls)}] Lade Liste von {url} herunter...")
        domains = fetch_list(url)
        all_domains.extend(domains)

    # Doppelte Einträge entfernen
    unique_domains = remove_duplicates(all_domains)

    with open(output_file, "w") as f:
        f.write("\n".join(sorted(unique_domains)))

    print(f"Bereinigte Blockliste mit {len(unique_domains)} Einträgen wurde in '{output_file}' gespeichert.")


def split():
    with open(output_file, 'rb') as f:
        part_number = 1
        while True:
            chunk = f.read(max_size)
            if not chunk:
                break
            part_name = f"{output_file}_part{part_number}"
            with open(part_name, 'wb') as part_file:
                part_file.write(chunk)
            part_number += 1
            print(f"Created {part_name}")


def main():
    # Downloaded alle Listen
    download()

    # Splittet die Datei, wenn sie zu gross ist einzelne Datein mit 100mb
    split()


if __name__ == "__main__":
    main()
