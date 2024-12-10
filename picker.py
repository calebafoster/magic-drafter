from superlist import SuperList
import random

class Picker:
    def __init__(self, path):
        self.working = SuperList(path)
        self.loaded_list = self.working.loaded_list

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

    def get_nonlands(self, color_identity):
        choices = []
        random.shuffle(self.loaded_list)

        for card in self.loaded_list:
            if 'Land' in card['type_line']:
                continue

            if not card['color_identity']:
                choices.append(card)
            else:
                viable = True
                for color in card['color_identity']:
                    if color not in color_identity:
                        viable = False
                        break
                if viable:
                    choices.append(card)

            if len(choices) >= 6:
                break

        return choices

if __name__ == "__main__":
    picker = Picker("commander-oracle-cards.json")
    choices = picker.get_commander_choices(6)
    names = [x["name"] for x in choices]
    print(names)
