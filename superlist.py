import json
import random
import time
import pprint

class SuperList:
    def __init__(self, path):
        self.loaded_list = self.get_json(path)
        random.shuffle(self.loaded_list)

    def get_json(self, path):
        with open(path, 'r', encoding="utf8") as f:
            file = json.load(f)
            return file

    def write_json(self, path, obj_list):
        with open(path, 'w', encoding="utf8") as f:
            json.dump(obj_list, f, indent=4)

#    def get_random_card(self):
#        r = requests.get("https://api.scryfall.com/cards/random")
#        return r.json()
#
#    def scryfall_lookup(self, name):
#        r = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={name}")
#        return r.json()

    def card_lookup(self, name):
        for card in self.loaded_list:
            if card["name"] == name:
                return card

        return list[0]

    def commander_cards(self, obj_list):
        legals = []

        for obj in obj_list:
            if obj["legalities"]["commander"] == "legal":
                print(f"{obj["name"]} is legal")
                legals.append(obj)

        print(len(legals))
        return legals


if __name__ == "__main__":
    s = SuperList('commander-oracle-cards.json')
    pprint.pprint(s.card_lookup('Expansion // Explosion'))
