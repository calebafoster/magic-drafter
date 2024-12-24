import requests
import urllib
import json

def download_oracle_cards():
    r = requests.get('https://api.scryfall.com/bulk-data')
    
    download_uri = r.json()['data'][0]['download_uri']

    urllib.request.urlretrieve(download_uri, 'oracle-cards.json')

def commander_cards(obj_list):
    legals = []

    for obj in obj_list:
        if obj["legalities"]["commander"] == "legal":
            print(f"{obj['name']} is legal")
            legals.append(obj)

    print(len(legals))
    return legals

def get_json(path):
    with open(path, 'r', encoding="utf8") as f:
        file = json.load(f)
        return file

def write_json(path, obj_list):
    with open(path, 'w', encoding="utf8") as f:
        json.dump(obj_list, f, indent=4)

if __name__ == "__main__":
    download_oracle_cards()
    loaded = get_json('oracle-cards.json')
    write_json('commander-oracle-cards.json', commander_cards(loaded))
