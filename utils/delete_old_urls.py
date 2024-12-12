from concurrent.futures import ThreadPoolExecutor
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
        print(f"Failed to load the JSON-file: {e}")
        return []


def check(url):
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return "404", url
        elif response.status_code == 200:
            return "200", url
        else:
            return f"Other: {response.status_code}", url
    except Exception as err:
        return f"Error: {err}", url


def main():
    # URLs aus der JSON-Datei laden
    list_urls = load_urls_from_json(json_file)
    if not list_urls:
        print("Failed to load urls from the JSON file.")
        return

    urls = []

    num_not_found = 0
    num_success = 0
    num_errors = 0

    print("Loading, this may take some time...")

    with ThreadPoolExecutor() as executor:
        results = executor.map(check, list_urls)

    for status, url in results:
        if status == "404":
            num_not_found += 1
            print(f"Failed to connect to {url}. Skipping... ERROR: 404")
        elif status == "200":
            num_success += 1
            print(f"{url} is OK (Status 200)")
            urls.append(url)
        else:
            num_errors += 1
            print(f"{url} - {status}")

    print(f"\nSummary:")
    print(f"URLs with 404: {num_not_found}")
    print(f"URLs OK (200): {num_success}")
    print(f"Other errors: {num_errors}")

    with open(json_file, 'w') as file:
        json.dump({"urls": urls},
                  file, indent=4)


if __name__ == "__main__":
    main()
