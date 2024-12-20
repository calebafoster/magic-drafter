import pygame
import sys

class Exporter:
    def __init__(self, deck):
        self.deck = deck
        self.string = ""

    def export(self):
        for card in self.deck:
            self.string += f"1 {card.dict['name']}\n"

        with open("deck.txt", 'w') as f:
            f.write(self.string)

        pygame.quit()
        sys.exit()
