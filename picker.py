from superlist import SuperList
import random

card_types = ["Land", "Creature", "Battle", "Sorcery", "Instant", "Planeswalker", "Artifact", "Enchantment"]

class Picker:
    def __init__(self, path):
        self.working = SuperList(path)
        self.loaded_list = self.working.loaded_list
        self.rarities = ['common', 'uncommon', 'rare', 'mythic']
        self.color_identity = ['W','U','B','R','G']

    def validate_rarity(self, card):
        for rarity in self.rarities:
            if rarity == card['rarity']:
                return True

        return False

    def validate_color_id(self, card):
        if 'color_identity' not in card:
            return True

        for color in card['color_identity']:
            if color not in self.color_identity:
                return False

        return True

    def set_rarities(self, rare_list = ['c','u','r','m']):
        self.rarities = []

        if 'c' in rare_list:
            self.rarities.append('common')
        if 'u' in rare_list:
            self.rarities.append('uncommon')
        if 'r' in rare_list:
            self.rarities.append('rare')
        if 'm' in rare_list:
            self.rarities.append('mythic')

    def get_commander_choices(self, opt_num):
        choices = []
        random.shuffle(self.loaded_list)

        for card in self.working.loaded_list:
            has_oracle = None

            if "oracle_text" in card:
                has_oracle = True
            else:
                has_oracle = False

            if "Legendary" in card["type_line"] and "Creature" in card["type_line"]:
                choices.append(card)
            elif has_oracle and "can be your commander" in card["oracle_text"]:
                choices.append(card)

            if len(choices) >= opt_num:
                break

        return choices

    def get_nonlands(self):
        choices = []

        random.shuffle(self.loaded_list)

        for card in self.loaded_list:
            viable = self.validate_rarity(card)

            if not viable:
                continue

            viable = self.validate_color_id(card)

            if not viable:
                continue

            if 'Land' in card['type_line']:
                continue

            if 'oracle_text' in card:
                if 'TK' in card['oracle_text']:
                    continue

            if 'Attraction' in card['type_line']:
                continue

            choices.append(card)

            if len(choices) >= 6:
                break

        return choices

    def get_lands(self):
        choices = []

        random.shuffle(self.loaded_list)

        for card in self.loaded_list:

            if 'Land' not in card['type_line']:
                continue

            if self.validate_rarity(card) and self.validate_color_id(card):
                choices.append(card)

            if len(choices) >= 6:
                break

        return choices


if __name__ == "__main__":
    picker = Picker("commander-oracle-cards.json")
    choices = picker.get_commander_choices(6)
    names = [x["name"] for x in choices]
    print(names)
