import pygame
import sys

map = {"W": "Plains", "U": "Island", "B": "Swamp", "R": "Mountain", "G": "Forest"}

class Exporter:
    def __init__(self, deck):
        self.deck = deck
        self.commander = self.deck[0]
        self.color_identity = self.commander.dict['color_identity']
        self.string = ""

    def export(self):
        for card in self.deck:
            self.string += f"1 {card.dict['name']}\n"

        with open(f"{self.commander.dict['name']}.txt", 'w') as f:
            f.write(self.string)

        pygame.quit()
        sys.exit()

    def basics_fill(self, deck_length):
        for i in range(deck_length - len(self.deck)):
            if len(self.color_identity):
                self.string += f"1 {map[self.color_identity[i % len(self.color_identity)]]}\n"
            else:
                self.string += "1 Wastes"
