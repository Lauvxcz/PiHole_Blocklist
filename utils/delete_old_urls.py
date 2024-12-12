import requests
import json

json_file = "../urls.json"


def load_urls_from_json(json_file):
    # Lädt die URLs aus der JSON-Datei.
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
            return data.get("urls", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Fehler beim Laden der JSON-Datei: {e}")
        return []


def check(url):
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return False
        elif response.status_code == 200:
            return True
        else:
            print(response.status_code)
            return False
    except ConnectionError:
        print(f"Failed to connect to {url}. Skipping...")
        return False


def main():
    # URLs aus der JSON-Datei laden
    list_urls = load_urls_from_json(json_file)
    if not list_urls:
        print("Keine gültigen URLs in der JSON-Datei gefunden.")
        return

    urls = []

    # Inhalte der Listen abrufen
    for index, url in enumerate(list_urls, 1):
        print(f"[{index}/{len(list_urls)}] Checking list from {url} ...")
        if check(url):
            urls.extend(url)

    print(urls)
    #with open(json_file, "w") as f:
    #    f.write("\n".join(urls))


if __name__ == "__main__":
    main()