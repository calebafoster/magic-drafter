import requests
import json
import pprint

r = requests.get("https://api.scryfall.com/cards/named?fuzzy=goblin archaeomancer")
my_dict = r.json()

def get_tts_deck(path):
    with open(path, 'r', encoding="utf8") as f:
        file = json.loads(f.read())
        file = pprint.pformat(file)
        return file

def write_tts_deck(path, obj):
    with open(path, 'w') as f:
        f.write(obj)

def get_json(path):
    with open(path, 'r', encoding="utf8") as f:
        file = json.load(f)
        return file

test = get_json("commander-oracle-cards.json")
count = 0
for obj in test:
    count = count + 1
